from orderbot.src.user import User
import os
import discord
from dotenv import load_dotenv, main
from discord.ext import commands
import re
from pathlib import Path

from orderbot.src.orderCtrl import OrderCtrl
from orderbot.src.userCtrl import UserCtrl
import orderbot.src.errors as errors
import orderbot.src.global_data as global_data
import orderbot.src.webOrderParser as webOrderParser
import orderbot.src.help_strs as help_strs

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

    bot = commands.Bot(command_prefix='!', description=description, intents=intents)

    @bot.event
    async def on_ready():    
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('Active Guilds:')
        [print(g.name) for g in bot.guilds]
        print('------')

    # TODO Handle variable arg length (both a single long string and cut up)
    # TODO output for Discord should look like the !list cmd, reuse?
    @bot.command(name='buy', 
        brief=help_strs.BUY_BRIEF_STR, 
        usage=help_strs.BUY_USAGE_STR, 
        help=help_strs.BUY_HELP_STR)
    async def add_order(ctx: commands.context.Context, *, arg: str):
        try:
            if valid_link(arg):
                item, count = webOrderParser.get_lsts_from_web_order(arg)
            else:
                count = re.findall(r'\d+', arg)
                count = [int(c) for c in count]
                item = re.findall(r'[a-zA-Z]+', arg)
            
            orderCtrl.add_order_from_lists(ctx.author.display_name, userCtrl, item, count)
            print(orderCtrl)

            # TODO Redo the respose for better Discord output
            reponse = 'buy command\n' + str(orderCtrl)
            # reponse = reponse + '\n'.join("{} ({})".format(item, amount) for item, amount in order.items())
        except errors.ReqUserNotRegistered:
            reponse = f"User **{ctx.author.display_name}** is not registered to make buy orders."

        await ctx.send(reponse)

    @bot.command(name='fill',
        brief=help_strs.FILL_BRIEF_STR,
        usage=help_strs.FILL_USAGE_STR,
        help=help_strs.FILL_HELP_STR)
    async def fill_order(ctx: commands.context.Context, in_identifier_args: str, order: str):
        try:
            found_maching_user = False
            for user in userCtrl.users:
                if in_identifier_args.isdigit():
                    if user.id == int(in_identifier_args):
                        user_name = user.name
                        found_maching_user = True
                        break
                else:
                    if user.alias == in_identifier_args or user.name == in_identifier_args:
                        user_name = user.name
                        found_maching_user = True
                        break

            if not found_maching_user:
                raise errors.IdentifierError
                

            if valid_link(order):
                item, count = webOrderParser.get_lsts_from_web_order(order)
            else:
                count = re.findall(r'\d+', order)
                count = [int(c) for c in count]
                item = re.findall(r'[a-zA-Z]+', order)

            # TODO Change this function to take either ID, Alisas or Name
            orderCtrl.fill_order_from_lists(user_name, item, count)
            reponse = '**Orders was filled.**\n\n'
            await ctx.send(reponse)
            await list_order(ctx)
            return
        except errors.IdentifierError:
            reponse = 'Invalid identifier, make sure it was spelled corretly and the user exits.'
        
        await ctx.send(reponse)


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
        for o in orderCtrl.orders:
            order_issuer: User = [u for u in userCtrl.users if o.user_name == u.name][0]
            response = response + (
                f'Issuer: **{order_issuer.name}** Alias: **{order_issuer.alias}**\n'
                f'Order ID: **{o.id}**\n```'
                )
            for item in o.items:
                response = response + (f'{item.count:7} - {item.name:25}\n')
            response = response + f'```'
            
        await ctx.send(response)

    @bot.command(name='cancelbuy',
        brief=help_strs.CANCELBUY_BRIEF_STR,
        usage=help_strs.CANCELBUY_USAGE_STR,
        help=help_strs.CANCELBUY_HELP_STR)
    async def cancle_order(ctx: commands.context.Context, id: int):
        orderCtrl.delete_order(id)
        reponse = f'**Orders with ID: {id} was canceled.**'
        await ctx.send(reponse)

    @bot.command(name='adduser',
        brief=help_strs.ADDUSER_BRIEF_STR,
        usage=help_strs.ADDUSER_USAGE_STR,
        help=help_strs.ADDUSER_HELP_STR)
    async def add_user(ctx: commands.context.Context, user_name: str, alias: str, priority: int, disc: str):
        try:
            userCtrl.add_user(user_name, ctx.author.display_name, alias=alias, priority=priority, discription=disc)
            response = (
                f"Added user **{userCtrl.users[-1].name}** "
                f"(alias:**{userCtrl.users[-1].alias}**) with "
                f"priority: **{userCtrl.users[-1].priority}** "
                f"and ID: **{userCtrl.users[-1].id}**.\n"
                f"Desctiption: *{userCtrl.users[-1].disc}*"
                )
        except errors.ReqUserNotRegistered:
            response = f"Could not add **{user_name}** you are not reqistered.\nUse the command: `!listusers` to see who can add a user."
        except errors.UserAlreadyRegistired:
            response = f"The user: **{user_name}** is already a registered user."

        await ctx.send(response)

    # TODO add remove by alias or ID
    @bot.command(name='removeuser',
        brief=help_strs.REMOVEUSER_BRIEF_STR,
        usage=help_strs.REMOVEUSER_USAGE_STR,
        help=help_strs.REMOVEUSER_HELP_STR)
    async def remove_user(ctx: commands.context.Context, *, user_name: str):
        try:
            userCtrl.remove_user(user_name)
            response = f"Removed user: **{user_name}**"
        except errors.ReqUserNotRegistered:
            response = f"Could not add **{user_name}** you are not reqistered.\nUse the command: `!listusers` to see who can add a user."
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

    bot.run(TOKEN)

if __name__ == "__main__":

    start_discord_bot()