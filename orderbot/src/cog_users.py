import re
import discord
from discord.ext import commands
import orderbot.src.help_strs as help_strs
# import orderbot.src.user_ctrl as userCtrl
import orderbot.src.database_ctrl as database_ctrl
from orderbot.src.database_ctrl import User
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
            # Test if the requesting member us registered, or is there is NO users
            if not database_ctrl.user_is_registered(discord_id = ctx.author.id) and not database_ctrl.table_is_empty(User):
                raise errors.ReqUserNotRegistered
            # Check if the user is already registered
            elif database_ctrl.user_is_registered(discord_id = member.id):
                raise errors.UserAlreadyRegistired

            database_ctrl.add_user(member, alias=alias, priority=priority, description=disc)
            with database_ctrl.get_user(discord_id = member.id) as user:
                response = (
                    f"Added user **{user.name}** "
                    f"(alias:**{user.alias}**) with "
                    f"priority: **{user.priority}** "
                    f"and ID: **{user.id}**.\n"
                    f"Description: *{user.disc}*"
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
            # Test if the requesting member us registered, or is there is NO users
            if not database_ctrl.user_is_registered(discord_id = ctx.author.id):
                raise errors.ReqUserNotRegistered
            # Check if the user is already registered
            elif not database_ctrl.user_is_registered(discord_id = member.id):
                raise errors.UserIsNotRegistired

            database_ctrl.delete_user(member)
            # userCtrl.remove_user(member, ctx.author)
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
        if not database_ctrl.table_is_empty(User):
            with database_ctrl.get_user() as users:
                if isinstance(users, User):
                    users = [users]
                for u in users:
                    response = response + (
                        f'{"Username: ":15}**{u.name}**\n'
                        f'{"Alias: ":22}**{u.alias}**\n'
                        f'{"ID: ":24}**{u.id}**\n'
                        f'{"Priority: ":21}**{u.priority}**\n'
                        f'{"Desciption: ":17}*{u.disc}*\n\n'
                        )
        else:
            response = response + f'There are not users!\nAdd one ;)'
        await ctx.send(response)