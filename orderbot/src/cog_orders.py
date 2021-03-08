import re
from orderbot.src.global_data import FILL_INPUT_TYPE
from discord.ext import commands
from discord.ext.commands.errors import MemberNotFound

import orderbot.src.help_strs as help_strs
import orderbot.src.errors as errors
import orderbot.src.orderCtrl as orderCtrl
import orderbot.src.userCtrl as userCtrl
import orderbot.src.validators as validators
import orderbot.src.webOrderParser as webOrderParser
import orderbot.src.cog_orders_functions as cog_orders_functions

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
    async def fill_order(self, ctx: commands.context.Context, *, args: str):
        try:
            # get all orders
            guild_orders = orderCtrl.get_orders(ctx.guild)
            if len(guild_orders) == 0:
                raise errors.OrderNonAvailableError

            input_type, data = cog_orders_functions.input_parser_fill(args)
            if input_type is None:
                raise errors.OrderInputError

            # Need to find the user in the ID, and if no id check for a single order only
            if input_type == FILL_INPUT_TYPE.ID_AND_LINK or input_type == FILL_INPUT_TYPE.ID_AND_SHORTHAND or input_type == FILL_INPUT_TYPE.ID_AND_P4TYPE:
                (data_id, data_str) = data
                #  Find memberm either from discord tags etc. or from user ID or alias
                found_maching_user = False
                try:
                    member = await commands.MemberConverter().convert(ctx, data_id)
                    user = userCtrl.get_user_from_member(member)
                    found_maching_user = True
                except MemberNotFound:
                    for user in userCtrl.users:
                        if data_id.isdigit():
                            if user.id == int(data_id):
                                user = userCtrl.get_user_by_id(int(data_id))
                                found_maching_user = True
                                break
                        else:
                            if user.alias.lower() == data_id.lower():
                                user = userCtrl.get_user_by_alias(data_id)
                                found_maching_user = True
                                break

                if not found_maching_user:
                    raise errors.IdentifierError
                
                if len([o for o in guild_orders if o.user == user]) == 0:
                    raise errors.OrderError

            elif input_type == FILL_INPUT_TYPE.ONLY_LINK or input_type == FILL_INPUT_TYPE.ONLY_SHORTHAND or input_type == FILL_INPUT_TYPE.ONLY_P4TYPE:
                if len(guild_orders) != 1:
                    raise errors.OrderMoreThanOneError

                user = guild_orders[0].user
                data_str = data

            item, count, remainder = cog_orders_functions.input_extractor_fill(input_type, data_str)

            if remainder != '':
                raise errors.OrderShorthandInputError
            
            # Create order to fill with, not items. Needed for later order tracking etc.
            filled_items = orderCtrl.fill_order_from_lists(user, item, count)
            response = '**Following items are accepted:**\n'
            response = response + f'```css\n'
            for item in filled_items:
                response = response + (f'{item.count:7} - {item.name:25}\n')
            response = response + f'```'
            await ctx.send(response)
            await self.list_order(ctx)
            return
        except errors.IdentifierError:
            response = 'Invalid identifier, make sure it was spelled correctly and the user exits.'
        except errors.OrderError:
            response = 'User does not have any orders.'
        except errors.OrderNonAvailableError:
            response = 'There are no active orders.'
        except errors.OrderMoreThanOneError:
            response = 'There are more than one order, please add an ID.'
        except errors.ItemOverFillError as e:
            response = f'***Error:*** The items in the order would be overfilled with the following items:```css\n'
            for item in e.item:
                response = response + f'{item.count:7} - {item.name:25}\n'
            response = response + f'```'
        except errors.ItemNotNeededError as e:
            response = f'***Error:*** The following items are not needed:```css\n'
            for item in e.item:
                response = response + f'{item.name}\n'
            response = response + f'```'
        except errors.OrderInputError:
            response = 'The order input could not be parsed. Please make sure there are no errors in the order. Otherwise contact Neorim#0099'
        except errors.OrderShorthandInputError:
            response = f'There was an error in the P4 shorthand\nThe erroneous part was:```'
            response = response + remainder
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