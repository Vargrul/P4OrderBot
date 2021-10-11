from discord.ext.commands import context
from orderbot.src.database_ctrl.ctrl import Session
import pytest
from sqlalchemy import select, exists
from datetime import datetime
from discord.ext import commands

from orderbot.src.global_data import StatusEnum, P4ItemEnum

import orderbot.src.database_ctrl as database_ctrl
from orderbot.src.database_ctrl import BuyOrder, Item

def test_add_buy_order(mocker, prep_db_add_test_user):
    ctx = mocker.Mock(spec=commands.Context)
    ctx.guild.id = 101
    ctx.guild.name = "test guild"
    ctx.channel.id = 201
    ctx.channel.name = "test channel"
    
    order_amount = None
    with database_ctrl.get_user(discord_id = 42) as user:
        # get the amount of orders currently related to the user
        order_amount = len(user.buy_orders)


        items = [
            Item(type = P4ItemEnum.SC,
                    quantity = 1000),
            Item(type = P4ItemEnum.SHPC,
                    quantity = 1000),
            Item(type = P4ItemEnum.BCN,
                    quantity = 1000),
            Item(type = P4ItemEnum.NF,
                    quantity = 1000)
        ]

        order_id = database_ctrl.add_buy_order(user, ctx, items)

    # Verify that there are now one more buy order
    with database_ctrl.get_user(discord_id = 42) as user:
        assert order_amount + 1 == len(user.buy_orders)


test_data = [
    {"status":StatusEnum.OPEN},
    # {"date_creation":},
    # {"date_closed":},
    {"guild_id":100},
    {"guild_name":"TestGuild"},
    {"channel_id":101},
    {"channel_name":"TestChannel"}
]
@pytest.mark.parametrize("input_dict", test_data)
def test_get_buy_order(input_dict, prep_db_add_test_user):
    with database_ctrl.get_buy_order(**input_dict) as Orders:
        assert Orders != None

# def test_to_discord_str():

def test_delete_buy_order(prep_db_add_test_user):
    assert False