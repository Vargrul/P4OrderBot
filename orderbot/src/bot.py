import os
from pathlib import Path

import discord
from discord.ext import commands

import orderbot.src.global_data as global_data

from orderbot.src.cog_users import CogUserCmds
from orderbot.src.cog_orders import CogOrderCmds
from orderbot.src.cog_misc import CogMiscCmds

from orderbot import __version__

class P4OrderBot():
    def __init__(self) -> None:

        # add cogs
        global_data.load_nonstatic_globals()
        self._TOKEN = os.getenv('DISCORD_TOKEN')

        self._init_misc()

        description = '''A bot to track PI4 orders!

        Contact Neorim#0099 if there is any problems.'''

        intents = discord.Intents.default()
        # intents.members = True

        self.bot = commands.Bot(command_prefix='!', description=description, intents=intents, case_insensitive=True)

        @self.bot.event
        async def on_command_error(ctx: commands.context.Context, exc: Exception):
            response = f"An error occurred. The error was:```{exc}```"
            await ctx.send(response)
            
        @self.bot.event
        async def on_ready():
            print('Logged in as')
            print(self.bot.user.name)
            print(self.bot.user.id)
            print('Active Guilds:')
            [print(g.name) for g in self.bot.guilds]
            # for g in bot.guilds:
            #     for c in g.text_channels:
            #         try:
            #             await c.send("I'm back online :smile:")
            #         except:
            #             pass
            print('------')

        self.bot.add_cog(CogMiscCmds(self.bot))
        self.bot.add_cog(CogUserCmds(self.bot))
        self.bot.add_cog(CogOrderCmds(self.bot))

    def _init_misc(self):
        Path(Path(__file__).parent / "data/").mkdir(exist_ok=True)

    def start(self):
        self.bot.run(self._TOKEN)