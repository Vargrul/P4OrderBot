import re

import discord
from discord.enums import Status
from orderbot.src.global_data import FILL_INPUT_TYPE, P4ItemEnum
from discord.ext import commands
from discord.ext.commands.errors import MemberNotFound

import orderbot.src.help_strs as help_strs
import orderbot.src.errors as errors
# import orderbot.src.order_ctrl as orderCtrl
# import orderbot.src.user_ctrl as userCtrl
import orderbot.src.validators as validators
import orderbot.src.web_order_parser as webOrderParser
import orderbot.src.cog_orders_functions as cog_orders_functions
import orderbot.src.database_ctrl as database_ctrl
from orderbot.src.database_ctrl import Item, StatusEnum
from sqlalchemy.orm import with_expression

class CogOrderCmds(commands.Cog, name="Order Commands"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='buy', 
        brief=help_strs.BUY_BRIEF_STR, 
        usage=help_strs.BUY_USAGE_STR, 
        help=help_strs.BUY_HELP_STR)
    async def add_order(self, ctx: commands.context.Context, *, arg: str):
        try:
            if not database_ctrl.user_is_registered(discord_id = ctx.author.id):
                raise errors.ReqUserNotRegistered
            # if not userCtrl.user_is_registered(ctx.author):
            #     raise errors.ReqUserNotRegistered
        
            
            if validators.valid_link(arg):
                item, count = webOrderParser.get_lsts_from_web_order(arg)
            elif validators.any_part_valid_shorthand_p4(arg.upper()):
                if validators.valid_shorthand_p4(arg.upper()):
                    item, count = validators.extract_shorthand_p4(arg.upper())
                else:
                    raise errors.OrderShorthandInputError
            else:
                raise errors.OrderInputError

            # Create item list
            items = []
            for itm, cnt in zip(item, count):
                items.append(Item.from_string_and_count(itm, cnt))
            # Add new order
            with database_ctrl.get_user(discord_id = ctx.author.id) as user:
                order_id = database_ctrl.add_buy_order(user, ctx, items)

            
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
            # Parse input args
            buyer_user_id, input_type, data_str = await cog_orders_functions.parse_fill_arg(ctx, args)
            # Extract data
            item, count, remainder = cog_orders_functions.input_extractor_fill(input_type, data_str)

            if remainder != '':
                raise errors.OrderShorthandInputError

            in_items = [Item.from_string_and_count(item, count) for item, count in zip(item, count)]

            # Do error checking
            # Concatenate all orders for the user for a Total needed list
            with database_ctrl.get_user(id = buyer_user_id) as user:
                needed_items_list = database_ctrl.total_items_wanted(user)
            
            # Error checking
            item_overfill = []
            item_not_needed = []
            for n_item in needed_items_list:
                for i_item in in_items:
                    if n_item.type == i_item.type:
                        if(i_item.quantity == None and n_item.quantity == 0) or (i_item.quantity != 0 and n_item.quantity == 0):
                            item_not_needed.append(i_item)
                        elif i_item.quantity != None:
                            if i_item.quantity > n_item.quantity:
                                item_overfill.append(i_item)
                        break

            if len(item_overfill) != 0:
                raise errors.ItemOverFillError(item_overfill)
            if len(item_not_needed) != 0:
                raise errors.ItemNotNeededError(item_not_needed)

            # Add new sell order
            #   This potentially need to be split in to smaller orders depending on the buying users orders as multiple can be filled at once.

            

            response = '**Following items are accepted:**\n'
            response = response + f'```css\n'
            for item in filled_items:
                response = response + (f'{item.count:7} - {item.name:25}\n')
            response = response + f'```'
            await ctx.send(response)
            await self.list_totals(ctx)
            return
        except errors.IdentifierError:
            response = 'Invalid identifier, make sure it was spelled correctly and the user exits.'
        except errors.OrderError:
            response = 'User does not have any orders.'
        except errors.OrderNonAvailableError:
            response = 'There are no active orders.'
        except errors.OrderMoreThanOneError:
            response = 'There are more than one user with orders, please add an ID.'
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
    async def list_totals(self, ctx: commands.context.Context):
        response = cog_orders_functions.list_response(ctx)
        await ctx.send(response)

    @commands.command(name='listorders',
        brief=help_strs.LIST_BRIEF_STR,
        usage=help_strs.LIST_USAGE_STR,
        help=help_strs.LIST_HELP_STR)
    async def list_order(self, ctx: commands.context.Context):
        response = cog_orders_functions.listorders_response(ctx)
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