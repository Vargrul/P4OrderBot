from typing import List, Pattern, Tuple
from discord import guild
from discord.ext.commands.errors import MemberNotFound
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import re
from pathlib import Path
import importlib.resources as pkg_resources

from orderbot.src.userCtrl import UserCtrl
from orderbot.src.orderCtrl import OrderCtrl
import orderbot.src.errors as errors
import orderbot.src.global_data as global_data
import orderbot.src.webOrderParser as webOrderParser
import orderbot.src.help_strs as help_strs
from orderbot import __version__

def valid_link(url: str):
    # validate web page test
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return regex.search(url)

def get_shorthand_regex(shorthand: str) -> Pattern:
    shorthand = shorthand.strip()
    if shorthand[0].isdigit():
        regex = re.compile(
            r'(\d+)\s*(\bSC\b|\bNF\b|\bIRD\b|\bOMA\b|\bBCN\b|\bSHPC\b|\bRCM\b|\bWM\b)\s*'
            )
    else:
        regex = re.compile(
            r'(\bSC\b|\bNF\b|\bIRD\b|\bOMA\b|\bBCN\b|\bSHPC\b|\bRCM\b|\bWM\b)\s*(\d+)\s*'
            )
    return regex

def valid_shorthand_p4(shorthand: str) -> bool:
    regex = get_shorthand_regex(shorthand)
    
    if len(regex.sub('', shorthand).strip()) == 0:
        return True
    else:
        return False

def extract_shorthand_p4(shorthand: str) -> Tuple[List[str], List[int]]:
    regex = get_shorthand_regex(shorthand)
    res = regex.findall(shorthand)

    shorthand = shorthand.strip()
    if shorthand[0].isdigit():
        str_lst = [s[1] for s in res]
        int_lst = [int(s[0]) for s in res]
    else:
        str_lst = [s[0] for s in res]
        int_lst = [int(s[1]) for s in res]
    return str_lst, int_lst

def _init_misc():
    Path(Path(__file__).parent / "data/").mkdir(exist_ok=True)

def start_discord_bot():
    global_data.load_nonstatic_globals()

    orderCtrl = OrderCtrl()
    orderCtrl.load_orders()
    userCtrl = UserCtrl()
    userCtrl.load_users()

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    _init_misc()

    description = '''A bot to track PI4 orders!

    Contact Neorim#0099 if there is any problems.'''

    intents = discord.Intents.default()
    # intents.members = True

    bot = commands.Bot(command_prefix='!', description=description, intents=intents, case_insensitive=True)

    @bot.event
    async def on_ready():    
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('Active Guilds:')
        [print(g.name) for g in bot.guilds]
        print('------')

    # TODO Handle variable arg length (both a single long string and cut up)
    @bot.command(name='buy', 
        brief=help_strs.BUY_BRIEF_STR, 
        usage=help_strs.BUY_USAGE_STR, 
        help=help_strs.BUY_HELP_STR)
    async def add_order(ctx: commands.context.Context, *, arg: str):
        try:
            if not userCtrl.user_is_registered(ctx.author):
                raise errors.ReqUserNotRegistered
        
            
            if valid_link(arg):
                item, count = webOrderParser.get_lsts_from_web_order(arg)
            elif valid_shorthand_p4(arg):
                item, count = extract_shorthand_p4(arg)
                # count = re.findall(r'\d+', order)
                # count = [int(c) for c in count]
                # item = re.findall(r'[a-zA-Z]+', order)
            else:
                raise errors.OrderInputError

            user = userCtrl.get_user_from_member(ctx.author)
            order = orderCtrl.add_order_from_lists(user, item, count, ctx.guild, ctx.channel)

            response = f"***The following buy order was added:***\n{order.to_discord_string()}"
            # response = 'buy command\n' + order.to_discord_string()
            
        except errors.ReqUserNotRegistered:
            response = f"User **{ctx.author.display_name}** is not registered to make buy orders."
        except errors.OrderInputError:
            response = 'The order input could not be parsed. Please make sure there is no errors in the order. Otherwise contact Neorim#0099'

        await ctx.send(response)

    @bot.command(name='fill',
        brief=help_strs.FILL_BRIEF_STR,
        usage=help_strs.FILL_USAGE_STR,
        help=help_strs.FILL_HELP_STR)
    async def fill_order(ctx: commands.context.Context, in_identifier_args, *, order: str):
        try:
            found_maching_user = False
            try:
                member = await commands.MemberConverter().convert(ctx, in_identifier_args)
                user = userCtrl.get_user_from_member(member)
                found_maching_user = True
            except MemberNotFound:
                for user in userCtrl.users:
                    if in_identifier_args.isdigit():
                        if user.id == int(in_identifier_args):
                            user = userCtrl.get_user_by_id(int(in_identifier_args))
                            found_maching_user = True
                            break
                    else:
                        if user.alias == in_identifier_args:
                            user = userCtrl.get_user_by_alias(in_identifier_args)
                            found_maching_user = True
                            break

            if not found_maching_user:
                raise errors.IdentifierError
            

            guild_orders = orderCtrl.get_orders(ctx.guild)
            if len([o for o in guild_orders if o.user == user]) == 0:
                raise errors.OrderError

            
            if valid_link(order):
                item, count = webOrderParser.get_lsts_from_web_order(order)
            elif valid_shorthand_p4(order):
                item, count = extract_shorthand_p4(order)
                # count = re.findall(r'\d+', order)
                # count = [int(c) for c in count]
                # item = re.findall(r'[a-zA-Z]+', order)
            else:
                raise errors.OrderInputError

            orderCtrl.fill_order_from_lists(user, item, count)
            response = '**Orders was filled.**\n\n'
            await ctx.send(response)
            await list_order(ctx)
            return
        except errors.IdentifierError:
            response = 'Invalid identifier, make sure it was spelled corretly and the user exits.'
        except errors.OrderError:
            response = 'User does not have any orders.'
        except errors.OrderInputError:
            response = 'The order input could not be parsed. Please make sure there is no errors in the order. Otherwise contact Neorim#0099'
        
        await ctx.send(response)


    @bot.command(name='cancelfill',
        brief=help_strs.CANCELFILL_BRIEF_STR,
        usage=help_strs.CANCELFILL_USAGE_STR,
        help=help_strs.CANCELFILL_HELP_STR)
    async def cancle_order(ctx: commands.context.Context, *, args):
        reponse = 'NOT IMPLEMENTED!\ncanclebuy command'
        await ctx.send(reponse)

    @bot.command(name='list',
        brief=help_strs.LIST_BRIEF_STR,
        usage=help_strs.LIST_USAGE_STR,
        help=help_strs.LIST_HELP_STR)
    async def list_order(ctx: commands.context.Context):
        # TODO Redo the response for better discord output
        response = "***Current outstanding orders:***\n"
        for o in orderCtrl.get_orders(ctx.guild):
            response = response + o.to_discord_string()
            
        await ctx.send(response)

    @bot.command(name='cancelbuy',
        brief=help_strs.CANCELBUY_BRIEF_STR,
        usage=help_strs.CANCELBUY_USAGE_STR,
        help=help_strs.CANCELBUY_HELP_STR)
    async def cancle_order(ctx: commands.context.Context, id: int):
        try:
            if not orderCtrl.check_order_id(id, ctx.guild):
                raise errors.OrderError

            orderCtrl.delete_order(id)
            reponse = f'**Orders with ID: {id} was canceled.**'
        except errors.OrderError:
            reponse = f'**Orders with ID: {id} does not exist! Please make sure the ID is correct.**'
        await ctx.send(reponse)

    @bot.command(name='adduser',
        brief=help_strs.ADDUSER_BRIEF_STR,
        usage=help_strs.ADDUSER_USAGE_STR,
        help=help_strs.ADDUSER_HELP_STR)
    async def add_user(ctx: commands.context.Context, member: discord.Member, alias: str, priority: int, disc: str):
        try:
            userCtrl.add_user(member, ctx.author, alias=alias, priority=priority, discription=disc)

            response = (
                f"Added user **{userCtrl.users[-1].name}** "
                f"(alias:**{userCtrl.users[-1].alias}**) with "
                f"priority: **{userCtrl.users[-1].priority}** "
                f"and ID: **{userCtrl.users[-1].id}**.\n"
                f"Desctiption: *{userCtrl.users[-1].disc}*"
                )
        except errors.ReqUserNotRegistered:
            response = f"Could not add **{member.display_name}**, as you are not reqistered.\nUse the command: `!listusers` to see who can add a user."
        except errors.UserAlreadyRegistired:
            response = f"The user: **{member.display_name}** is already a registered user."

        await ctx.send(response)

    # TODO add remove by alias or ID
    @bot.command(name='removeuser',
        brief=help_strs.REMOVEUSER_BRIEF_STR,
        usage=help_strs.REMOVEUSER_USAGE_STR,
        help=help_strs.REMOVEUSER_HELP_STR)
    async def remove_user(ctx: commands.context.Context, *, member: discord.Member):
        try:
            userCtrl.remove_user(member, ctx.author)
            response = f"Removed user: **{member.display_name}**"
        except errors.ReqUserNotRegistered:
            response = f"Could not remove **{member.display_name}** you are not reqistered.\nUse the command: `!listusers` to see who can add a user."
        except errors.UserIsNotRegistired:
            response = f"Could not find user.\nPlease check the username is correct."
            
        await ctx.send(response)

    @bot.command(name='listusers',
        brief=help_strs.LISTUSERS_BRIEF_STR,
        usage=help_strs.LISTUSERS_USAGE_STR,
        help=help_strs.LISTUSERS_HELP_STR)
    async def list_users(ctx: commands.context.Context):
        response = "***Current registered users(buyers):***\n"
        for u in userCtrl.users:
            response = response + (
                f'{"Username: ":15}**{u.name}**\n'
                f'{"Alias: ":22}**{u.alias}**\n'
                f'{"ID: ":24}**{u.id}**\n'
                f'{"Priority: ":21}**{u.priority}**\n'
                f'{"Desciption: ":17}*{u.disc}*\n\n'
                )
        await ctx.send(response)

    @bot.command(name='version',
        brief=help_strs.VERSION_BRIEF_STR,
        usage=help_strs.VERSION_USAGE_STR,
        help=help_strs.VERSION_HELP_STR)
    async def cmd_version(ctx: commands.context.Context):
        response = (f"Bot version: {__version__}\n")
        response = response + f"```"
        response = response + pkg_resources.read_text(__package__, 'CHANGELOG.md')
        response = response + f"```"
        await ctx.send(response)

    bot.run(TOKEN)

if __name__ == "__main__":
    start_discord_bot()
