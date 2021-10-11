from typing import List, Union
import discord
import discord.ext.commands as commands
from discord.ext.commands import Context
from orderbot.src.global_data import FILL_INPUT_TYPE, StatusEnum
import orderbot.src.validators as validators
import orderbot.src.regexes as regexes
import orderbot.src.web_order_parser as webOrderParser
import orderbot.src.database_ctrl as database_ctrl
from orderbot.src.database_ctrl import User, Item, BuyOrder, SellOrder
import orderbot.src.errors as errors
# import orderbot.src.order_ctrl as orderCtrl
# import orderbot.src.user_ctrl as userCtrl

def input_parser_fill(arg_str: str):
    input_type = None
    if validators.valid_id_and_link(arg_str):
        input_type = FILL_INPUT_TYPE.ID_AND_LINK
        output_data = regexes.regex_id_and_link().match(arg_str).groups()
        output_data = (output_data[0].replace('\"', ''), output_data[1])
    elif validators.valid_id_and_shorthand(arg_str):
        input_type = FILL_INPUT_TYPE.ID_AND_SHORTHAND
        output_data = regexes.regex_id_and_shorthand().match(arg_str).groups()
        output_data = (output_data[0].replace('\"', ''), output_data[1])
    elif validators.valid_id_and_p4type(arg_str):
        input_type = FILL_INPUT_TYPE.ID_AND_P4TYPE
        output_data = regexes.regex_id_and_p4type().match(arg_str).groups()
        output_data = (output_data[0].replace('\"', ''), output_data[1])
    elif validators.valid_link(arg_str):
        input_type = FILL_INPUT_TYPE.ONLY_LINK
        output_data = arg_str
    elif validators.valid_shorthand(arg_str):
        input_type = FILL_INPUT_TYPE.ONLY_SHORTHAND
        output_data = arg_str
    elif validators.valid_p4type(arg_str):
        input_type = FILL_INPUT_TYPE.ONLY_P4TYPE
        output_data = arg_str
    
    return input_type, output_data

def input_extractor_fill(input_type: FILL_INPUT_TYPE, data: str):
    if input_type == FILL_INPUT_TYPE.ID_AND_SHORTHAND or input_type == FILL_INPUT_TYPE.ONLY_SHORTHAND:
        if data[0].isdigit():
            regex = regexes.regex_extract_shorthand()
        else:
            regex = regexes.regex_extract_shorthand_reverse()
        res = regex.findall(data.upper())

        if res[0][0].isdigit():
            count = [int(c[0]) for c in res[:]]
            shorthand = [c[1] for c in res[:]]
        else:
            shorthand = [c[0] for c in res[:]]
            count = [int(c[1]) for c in res[:]]

        remainder = regex.sub('', data).strip()
    elif input_type == FILL_INPUT_TYPE.ID_AND_P4TYPE or input_type == FILL_INPUT_TYPE.ONLY_P4TYPE:
        regex = regexes.regex_extract_p4types()

        shorthand = regex.findall(data.upper())
        count = [None] * len(shorthand)
        remainder = regex.sub('', data).strip()
    elif input_type == FILL_INPUT_TYPE.ID_AND_LINK or input_type == FILL_INPUT_TYPE.ONLY_LINK:
        shorthand, count = webOrderParser.get_lsts_from_web_order(data)
        remainder = ''

    return shorthand, count, remainder

def fill_orders(buy_user: User, sell_user: User, in_items: List[Item]) -> List[int]:
    # Get all users orders

    # Fill what is possible and make multiple sell orders per buy order

    # return order id(s)
    pass

def list_response(ctx: Context) -> str:
    response = "**Current** ***TOTAL*** ** items wanted per buyer:**\n"

    for user in userCtrl.users:
        if len(orderCtrl.get_orders(guild=ctx.guild, user=user)) != 0:
            response = response + orderCtrl.user_total_orders_to_discord_string(user, guild=ctx.guild)
            response = response + f'\n'
    
    return response

def listorders_response(ctx: Context) -> str:
    orders = orderCtrl.get_orders(guild=ctx.guild)

    response = f'**Current outstanding orders:**\n'
    for o in orders:
        response = response + o.to_discord_string() + f'\n'

    return response

async def parse_fill_arg(ctx: Context, arg_str: str) -> Union[int, FILL_INPUT_TYPE, str]:
    user_id = None
    # get all orders
    with database_ctrl.get_buy_order(guild_id=ctx.guild.id, status=StatusEnum.OPEN) as guild_orders:
        if len(guild_orders) == 0:
            raise errors.OrderNonAvailableError

        input_type, data = input_parser_fill(arg_str)
        if input_type is None:
            raise errors.OrderInputError

        # Need to find the user in the ID, and if no id check for a single order only
        if input_type == FILL_INPUT_TYPE.ID_AND_LINK or input_type == FILL_INPUT_TYPE.ID_AND_SHORTHAND or input_type == FILL_INPUT_TYPE.ID_AND_P4TYPE:
            (data_id, data_str) = data
            #  Find memberm either from discord tags etc. or from user ID or alias
            found_maching_user = False
            try:
                member = await commands.MemberConverter().convert(ctx, data_id)
                # user = data.get_user_from_member(member)
                with database_ctrl.get_user(discord_id = member.id) as user:
                    user_id = user.id
                found_maching_user = True
            except discord.errors.MemberNotFound:
                # with database_ctrl.get_user() as users:
                #     for user in users:
                        if data_id.isdigit():
                            # if user.id == int(data_id):
                            if database_ctrl.user_is_registered(id=data_id):
                                user_id = data_id
                                # user = userCtrl.get_user_by_id(int(data_id))
                                found_maching_user = True
                        else:
                            if database_ctrl.user_is_registered(alias = data_id):
                                with database_ctrl.get_user(alias = data_id) as user:
                                    user_id = user.id
                                # user = userCtrl.get_user_by_alias(data_id)
                                found_maching_user = True

            if not found_maching_user:
                raise errors.IdentifierError
            
            with database_ctrl.get_buy_order(id = user_id) as user_orders:
                if len(user_orders) == 0:
                    raise errors.OrderError

        elif input_type == FILL_INPUT_TYPE.ONLY_LINK or input_type == FILL_INPUT_TYPE.ONLY_SHORTHAND or input_type == FILL_INPUT_TYPE.ONLY_P4TYPE:
            unique_active_buyers = []   
            for o in guild_orders:
                if not o.user.id in unique_active_buyers:
                    unique_active_buyers.append(o.user.id)

            if len(unique_active_buyers) != 1:
                raise errors.OrderMoreThanOneError

            user_id = guild_orders[0].user.id
            data_str = data

    return user_id, input_type, data_str