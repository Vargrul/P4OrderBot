import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import re

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

@bot.command(name='buy')
async def add_order(ctx, order: str):
    counts = re.findall(r'([A-Z])\w+', order)
    print(order)
    reponse = 'buy command\n' + ', '.join(counts)
    await ctx.send(reponse)

@bot.command(name='fill')
async def fill_order(ctx):
    reponse = 'fill command'
    await ctx.send(reponse)

@bot.command(name='canclefill')
async def fill_order(ctx):
    reponse = 'canclefill command'
    await ctx.send(reponse)

@bot.command(name='list')
async def fill_order(ctx):
    reponse = 'list command'
    await ctx.send(reponse)

@bot.command(name='canclebuy')
async def fill_order(ctx):
    reponse = 'canclebuy command'
    await ctx.send(reponse)


bot.run(TOKEN)