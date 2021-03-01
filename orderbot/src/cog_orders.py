from discord.ext import commands
from discord.ext.commands.errors import MemberNotFound

import orderbot.src.help_strs as help_strs
import orderbot.src.errors as errors
import orderbot.src.orderCtrl as orderCtrl
import orderbot.src.userCtrl as userCtrl
import orderbot.src.validators as validators
import orderbot.src.webOrderParser as webOrderParser

class CogOrderCmds(commands.Cog, name="Order Commands"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='buy', 
        brief=help_strs.BUY_BRIEF_STR, 
        usage=help_strs.BUY_USAGE_STR, 
        help=help_strs.BUY_HELP_STR)
    async def add_order(self, ctx: commands.context.Context, *, arg: str):
        try:
            if not userCtrl.user_is_registered(ctx.author):
                raise errors.ReqUserNotRegistered
        
            
            if validators.valid_link(arg):
                item, count = webOrderParser.get_lsts_from_web_order(arg)
            elif validators.any_part_valid_shorthand_p4(arg.upper()):
                if validators.valid_shorthand_p4(arg.upper()):
                    item, count = validators.extract_shorthand_p4(arg.upper())
                else:
                    raise errors.OrderShorthandInputError
            else:
                raise errors.OrderInputError

            user = userCtrl.get_user_from_member(ctx.author)
            order = orderCtrl.add_order_from_lists(user, item, count, ctx.guild, ctx.channel)

            response = f"***The following buy order was added:***\n{order.to_discord_string()}"
            # response = 'buy command\n' + order.to_discord_string()
            
        except errors.ReqUserNotRegistered:
            response = f"User **{ctx.author.display_name}** is not registered to make buy orders."
        except errors.OrderInputError:
            response = 'The order input could not be parsed. Please make sure there are no errors in the order. Otherwise contact Neorim#0099'
        except errors.OrderShorthandInputError:
            response = f'There was an error in the P4 shorthand\nThe erroneous part was:```'
            response = response + validators.extract_invalid_part_shorthand_p4(arg.upper())
            response = response + f"```"

        await ctx.send(response)

    @commands.command(name='fill',
        brief=help_strs.FILL_BRIEF_STR,
        usage=help_strs.FILL_USAGE_STR,
        help=help_strs.FILL_HELP_STR)
    async def fill_order(self, ctx: commands.context.Context, in_identifier_args, *, order: str):
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
                        if user.alias.lower() == in_identifier_args.lower():
                            user = userCtrl.get_user_by_alias(in_identifier_args)
                            found_maching_user = True
                            break

            if not found_maching_user:
                raise errors.IdentifierError
            

            guild_orders = orderCtrl.get_orders(ctx.guild)
            if len([o for o in guild_orders if o.user == user]) == 0:
                raise errors.OrderError

            
            if validators.valid_link(order):
                item, count = webOrderParser.get_lsts_from_web_order(order)
            elif validators.any_part_valid_shorthand_p4(order.upper()):
                if validators.valid_shorthand_p4(order.upper()):
                    item, count = validators.extract_shorthand_p4(order.upper())
                else:
                    raise errors.OrderShorthandInputError
            else:
                raise errors.OrderInputError

            orderCtrl.fill_order_from_lists(user, item, count)
            response = '**Orders was filled.**\n\n'
            await ctx.send(response)
            await self.list_order(ctx)
            return
        except errors.IdentifierError:
            response = 'Invalid identifier, make sure it was spelled correctly and the user exits.'
        except errors.OrderError:
            response = 'User does not have any orders.'
        except errors.OrderInputError:
            response = 'The order input could not be parsed. Please make sure there are no errors in the order. Otherwise contact Neorim#0099'
        except errors.OrderShorthandInputError:
            response = f'There was an error in the P4 shorthand\nThe erroneous part was:```'
            response = response + validators.extract_invalid_part_shorthand_p4(order.upper())
            response = response + f"```"

        await ctx.send(response)


    @commands.command(name='cancelfill',
        brief=help_strs.CANCELFILL_BRIEF_STR,
        usage=help_strs.CANCELFILL_USAGE_STR,
        help=help_strs.CANCELFILL_HELP_STR)
    async def cancel_order(self, ctx: commands.context.Context, *, args):
        response = 'NOT IMPLEMENTED!\ncancelbuy command'
        await ctx.send(response)

    @commands.command(name='list',
        brief=help_strs.LIST_BRIEF_STR,
        usage=help_strs.LIST_USAGE_STR,
        help=help_strs.LIST_HELP_STR)
    async def list_order(self, ctx: commands.context.Context):
        # TODO Redo the response for better discord output
        response = "***Current outstanding orders:***"
        orders = orderCtrl.get_orders(ctx.guild)
        if len(orders) == 0:
            response = response + f" __***None***__"
        else:
            for o in orders:
                response = response + f'\n' + o.to_discord_string()
            
        await ctx.send(response)

    @commands.command(name='cancelbuy',
        brief=help_strs.CANCELBUY_BRIEF_STR,
        usage=help_strs.CANCELBUY_USAGE_STR,
        help=help_strs.CANCELBUY_HELP_STR)
    async def cancel_order(self, ctx: commands.context.Context, id: int):
        try:
            if not orderCtrl.check_order_id(id, ctx.guild):
                raise errors.OrderError

            orderCtrl.delete_order(id)
            response = f'**Orders with ID: {id} was canceled.**'
        except errors.OrderError:
            response = f'**Orders with ID: {id} does not exist! Please make sure the ID is correct.**'
        await ctx.send(response)