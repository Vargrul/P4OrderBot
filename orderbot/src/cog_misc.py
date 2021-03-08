import importlib.resources as pkg_resources

from discord.ext import commands

from orderbot import __version__
import orderbot.src.help_strs as help_strs

class CogMiscCmds(commands.Cog, name="Misc Commands"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='version',
        brief=help_strs.VERSION_BRIEF_STR,
        usage=help_strs.VERSION_USAGE_STR,
        help=help_strs.VERSION_HELP_STR)
    async def cmd_version(self, ctx: commands.context.Context):
        response = (f"Bot version: {__version__}\n")
        response = response + f"```"
        response = response + pkg_resources.read_text('orderbot', 'CHANGELOG.md')
        response = response + f"```"
        await ctx.send(response)