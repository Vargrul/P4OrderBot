from orderbot.src.user import User
import os
import discord
from dotenv import load_dotenv, main
from discord.ext import commands
import re

from orderbot.src.orderCtrl import OrderCtrl
from orderbot.src.userCtrl import UserCtrl
import orderbot.src.errors as errors
import orderbot.src.global_data as global_data
import orderbot.src.webOrderParser as webOrderParser

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


def start_discord_bot():
    global_data.load_nonstatic_globals()

    orderCtrl = OrderCtrl()
    orderCtrl.load_orders()
    userCtrl = UserCtrl()
    userCtrl.load_users()

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

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
    @bot.command(name='buy')
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

    # TODO add id and alias as usabel name, is currently not working
    @bot.command(name='fill')
    async def fill_order(ctx: commands.context.Context, in_identifier_args: str, *, order: str):
        identifier_args = re.findall(r'\w+', in_identifier_args)
        if len(identifier_args) == 1:
            user_name = identifier_args[0]
        elif len(identifier_args) == 2:
            if identifier_args[0].lower() == 'alias':
                for user in userCtrl.users:
                    if user.alias == identifier_args[1]:
                        user_name = user.name
            elif identifier_args[0].lower() == 'id':
                for user in userCtrl.users:
                    if user.id == int(identifier_args[1]):
                        user_name = user.name
            else:
                reponse = 'Invalid identifier args.'
                await ctx.send(reponse)
                return

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

    @bot.command(name='cancelfill')
    async def cancle_order(ctx: commands.context.Context, *, args):
        reponse = 'NOT IMPLEMENTED!\ncanclebuy command'
        await ctx.send(reponse)

    @bot.command(name='list')
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
            
                
        # for o in orderCtrl.orders:
        #     response = response + f"{str(o)}\n"
        await ctx.send(response)

    @bot.command(name='cancelbuy')
    async def cancle_order(ctx: commands.context.Context, id: int):
        orderCtrl.delete_order(id)
        reponse = f'**Orders with ID: {id} was canceled.**'
        await ctx.send(reponse)

    @bot.command(name='adduser')
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

    @bot.command(name='removeuser')
    async def remove_user(ctx: commands.context.Context, *, user_name: str):
        try:
            userCtrl.remove_user(user_name)
            response = f"Removed user: **{user_name}**"
        except errors.ReqUserNotRegistered:
            response = f"Could not add **{user_name}** you are not reqistered.\nUse the command: `!listusers` to see who can add a user."
        except errors.UserIsNotRegistired:
            response = f"Could not find user.\nPlease check the username is correct."
            
        await ctx.send(response)

    @bot.command(name='listusers')
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