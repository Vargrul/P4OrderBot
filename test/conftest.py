from orderbot.src.database_ctrl.ctrl import user_is_registered
from orderbot.src.database_ctrl import buy_order, sell_order
import pytest
import discord
from datetime import datetime

from sqlalchemy import select
from sqlalchemy import inspect

import orderbot.src.database_ctrl as database_ctrl
from orderbot.src.database_ctrl import User, BuyOrder, SellOrder, Item
from orderbot.src.global_data import StatusEnum, P4ItemEnum

@pytest.fixture()
def clean_db():
    yield

    with database_ctrl.Session() as session:
        results = session.execute(select(User))
        users = results.scalars().all()
        for user in users:
            session.delete(user)

        results = session.execute(select(BuyOrder))
        buy_orders = results.scalars().all()
        for bo in buy_orders:
            session.delete(bo)

        results = session.execute(select(SellOrder))
        sell_orders = results.scalars().all()
        for so in sell_orders:
            session.delete(so)

        results = session.execute(select(Item))
        items = results.scalars().all()
        for i in items:
            session.delete(i)

        session.commit()

@pytest.fixture()
def prep_db_add_test_user(clean_db):
    user = User(name='Test', 
                priority=2, 
                disc='test disc', 
                alias='test', 
                discord_id=42, 
                discord_name='Test',
                discord_discriminator='Test#0099')

    bo1 = BuyOrder(status = StatusEnum.OPEN,
                  date_creation = datetime.now(),
                  date_closed = None,
                  guild_id = 100,
                  guild_name = 'TestGuild',
                  channel_id = 101,
                  channel_name = 'TestChannel',

                  user = user)

    item1 = Item(type = P4ItemEnum.SC,
                 quantity = 1000,
                 buy_order = bo1)
    item2 = Item(type = P4ItemEnum.SHPC,
                 quantity = 1000,
                 buy_order = bo1)
    item3 = Item(type = P4ItemEnum.BCN,
                 quantity = 1000,
                 buy_order = bo1)
    item4 = Item(type = P4ItemEnum.NF,
                 quantity = 1000,
                 buy_order = bo1)
    
    so1 = SellOrder(date_creation = datetime.now(),
                    guild_id = 100,
                    guild_name = 'TestGuild',
                    channel_id = 101,
                    channel_name = 'TestChannel',

                    user = user,
                    buy_order = bo1
                    )

    s_item1 = Item(type = P4ItemEnum.SC,
                 quantity = 100,
                 sell_order = so1)
    s_item2 = Item(type = P4ItemEnum.SHPC,
                 quantity = 100,
                 sell_order = so1)
    s_item3 = Item(type = P4ItemEnum.BCN,
                 quantity = 100,
                 sell_order = so1)
    s_item4 = Item(type = P4ItemEnum.NF,
                 quantity = 100,
                 sell_order = so1)
                

    
    with database_ctrl.Session() as session:
        session.add(user)
        session.commit()

    yield

    # with database_ctrl.Session() as session:
    #     results = session.execute(select(User))
    #     users = results.scalars().all()
    #     for user in users:
    #         session.delete(user)
    #         session.commit()

            
@pytest.fixture()
def discord_member_clean(mocker):
    disc_member = mocker.Mock(spec=discord.Member)
    return disc_member

# Testcases:
# 1: If no user is in the DB accept any requesting user, using minimal input
# 2: Use the first added user to add a new user
# 3: Use an invalid user to try and add an user
test_data = [
    (('TestUser2 Disp', 'Test'),
     (987654321, 42),
     ('TestUser2', 'Test'),
     ('TestUser2#0002', 'Test#0099#0001'),
     3,
     "new test user created by first",
     "Test2",
     True
    ),

    (('TestUser3 Disp', 'ReqUserNotReged Disp'),
     (555444666, 147852369),
     ('TestUser3', 'ReqUserNotReged'),
     ('TestUser3#0003', 'ReqUserNotReged#0000'),
     5,
     "",
     None,
     False
    ),
]
@pytest.fixture(params=test_data)
def add_user_data_fixture(mocker, request):
    d1 = mocker.Mock(spec=discord.Member)
    d2 = mocker.Mock(spec=discord.Member)

    d1.display_name = request.param[0][0]
    d1.id = request.param[1][0]
    d1.name = request.param[2][0]
    d1.discriminator = request.param[3][0]
    
    d2.display_name = request.param[0][1]
    d2.id = request.param[1][1]
    d2.name = request.param[2][1]
    d2.discriminator = request.param[3][1]

    yield d1, d2, request.param[4], request.param[5], request.param[6], request.param[7]