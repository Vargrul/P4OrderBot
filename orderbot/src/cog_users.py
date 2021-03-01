import discord
from discord.ext import commands
import orderbot.src.help_strs as help_strs
import orderbot.src.userCtrl as userCtrl
import orderbot.src.errors as errors
    
class CogUserCmds(commands.Cog, name="User Commands"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='adduser',
        brief=help_strs.ADDUSER_BRIEF_STR,
        usage=help_strs.ADDUSER_USAGE_STR,
        help=help_strs.ADDUSER_HELP_STR)
    async def add_user(self, ctx: commands.context.Context, member: discord.Member, alias: str, priority: int, disc: str):
        try:
            userCtrl.add_user(member, ctx.author, alias=alias, priority=priority, discription=disc)

            response = (
                f"Added user **{userCtrl.users[-1].name}** "
                f"(alias:**{userCtrl.users[-1].alias}**) with "
                f"priority: **{userCtrl.users[-1].priority}** "
                f"and ID: **{userCtrl.users[-1].id}**.\n"
                f"Description: *{userCtrl.users[-1].disc}*"
                )
        except errors.ReqUserNotRegistered:
            response = f"Could not add **{member.display_name}**, as you are not registered.\nUse the command: `!listusers` to see who can add a user."
        except errors.UserAlreadyRegistired:
            response = f"The user: **{member.display_name}** is already a registered user."

        await ctx.send(response)

    # TODO add remove by alias or ID
    @commands.command(name='removeuser',
        brief=help_strs.REMOVEUSER_BRIEF_STR,
        usage=help_strs.REMOVEUSER_USAGE_STR,
        help=help_strs.REMOVEUSER_HELP_STR)
    async def remove_user(self, ctx: commands.context.Context, *, member: discord.Member):
        try:
            userCtrl.remove_user(member, ctx.author)
            response = f"Removed user: **{member.display_name}**"
        except errors.ReqUserNotRegistered:
            response = f"Could not remove **{member.display_name}** you are not registered.\nUse the command: `!listusers` to see who can add a user."
        except errors.UserIsNotRegistired:
            response = f"Could not find user.\nPlease check the username is correct."
            
        await ctx.send(response)

    @commands.command(name='listusers',
        brief=help_strs.LISTUSERS_BRIEF_STR,
        usage=help_strs.LISTUSERS_USAGE_STR,
        help=help_strs.LISTUSERS_HELP_STR)
    async def list_users(self, ctx: commands.context.Context):
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