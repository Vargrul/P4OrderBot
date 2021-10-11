import builtins
from contextlib import contextmanager
from datetime import datetime
import os
from typing import ContextManager, ItemsView, List, Union

import discord
from discord.ext import commands

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import select, exists
from sqlalchemy.sql.selectable import Exists

from orderbot.src.global_data import P4ItemEnum, StatusEnum
from .user import User
from .item import Item
from .buy_order import BuyOrder
from .sell_order import SellOrder
from .base import Base

import orderbot.src.errors as error

DATABASE_URI = os.getenv('DATABASE_URI')

__engine = create_engine(DATABASE_URI, future=True)
Base.metadata.create_all(__engine)

Session = sessionmaker(__engine)
Session.expire_on_commit = False
# session = Session()

@contextmanager
def get_buy_order(session: Session = None,
                  id: Union[int, List[int]] = None,
                  user_id: Union[int, List[int]] = None,
                  status: Union[StatusEnum, List[StatusEnum]] = None,
                  date_creation: Union[datetime, List[datetime]] = None,
                  date_closed: Union[datetime, List[datetime]] = None,
                  guild_id: Union[int, List[int]] = None,
                  guild_name: Union[str, List[str]] = None,
                  channel_id: Union[int, List[int]] = None,
                  channel_name: Union[str, List[str]] = None
                  ) -> ContextManager[Union[SellOrder, List[SellOrder]]]:
    if all(v is None for v in {id, user_id, status, date_creation, date_closed, guild_id, guild_name, channel_id, channel_name}):
        raise ValueError('Expected at least one argument to be input.')

    conditions = []
    if not id == None:
        if isinstance(id, int):
            conditions.append(BuyOrder.id == id)
        else:
            [conditions.append(BuyOrder.id == d_id) for d_id in id]
    if not user_id == None:
        if isinstance(user_id, int):
            conditions.append(BuyOrder.user_id == user_id)
        else:
            [conditions.append(BuyOrder.user_id == arg) for arg in user_id]
    if not status == None:
        if isinstance(status, StatusEnum):
            conditions.append(BuyOrder.status == status)
        else:
            [conditions.append(BuyOrder.status == arg) for arg in status]
    if not date_creation == None:
        if isinstance(date_creation, datetime):
            conditions.append(BuyOrder.date_creation == date_creation)
        else:
            [conditions.append(BuyOrder.date_creation == arg) for arg in date_creation]
    if not date_closed == None:
        if isinstance(date_closed, datetime):
            conditions.append(BuyOrder.date_closed == date_closed)
        else:
            [conditions.append(BuyOrder.date_closed == arg) for arg in date_closed]
    if not guild_id == None:
        if isinstance(guild_id, int):
            conditions.append(BuyOrder.guild_id == guild_id)
        else:
            [conditions.append(BuyOrder.guild_id == arg) for arg in guild_id]
    if not guild_name == None:
        if isinstance(guild_name, str):
            conditions.append(BuyOrder.guild_name == guild_name)
        else:
            [conditions.append(BuyOrder.guild_name == arg) for arg in guild_name]
    if not channel_id == None:
        if isinstance(channel_id, int):
            conditions.append(BuyOrder.channel_id == channel_id)
        else:
            [conditions.append(BuyOrder.channel_id == arg) for arg in channel_id]
    if not channel_name == None:
        if isinstance(channel_name, str):
            conditions.append(BuyOrder.channel_name == channel_name)
        else:
            [conditions.append(BuyOrder.channel_name == arg) for arg in channel_name]

    with (Session() if session == None else session) as local_session:
        sell_order = local_session.execute(select(BuyOrder).where(*conditions)).all()
        if len(sell_order) == 1:
            yield sell_order[0][0]
        else: 
            yield sell_order[0]

        if session == None:
            local_session.commit()
        else:
            local_session.flush()

# TODO Move access request out of this function!
    # Test if the requesting member us registered, or is there is NO users
    # if not user_is_registered(requesting_member) and not table_is_empty(User):
    #     raise error.ReqUserNotRegistered
    # # Check if the user is already registered
    # elif user_is_registered(member):
    #     raise error.UserAlreadyRegistired
def add_buy_order(user: User, ctx: commands.context.Context, items: List[Item], status: StatusEnum = StatusEnum.OPEN, date_creation:datetime = datetime.now(), date_closed: datetime = None) -> int:
    
    bo1 = BuyOrder(status = status,
                   date_creation = date_creation,
                   date_closed = date_closed,
                   guild_id = ctx.guild.id,
                   guild_name = ctx.guild.name,
                   channel_id = ctx.channel.id,
                   channel_name = ctx.channel.name,
   
                   user = user,
                   items = items
                   )
    session = Session.object_session(user)
    session.flush()

    return bo1.id

@contextmanager
def get_sell_order(session: Session = None,
                   id: Union[int, List[int]] = None,
                   buy_order_id: Union[int, List[int]] = None,
                   user_id: Union[int, List[int]] = None,
                   date_creation: Union[datetime, List[datetime]] = None,
                   guild_id: Union[int, List[int]] = None,
                   guild_name: Union[str, List[str]] = None,
                   channel_id: Union[int, List[int]] = None,
                   channel_name: Union[str, List[str]] = None
                   ) -> ContextManager[Union[SellOrder, List[SellOrder]]]:
    if all(v is None for v in {id, buy_order_id, user_id, date_creation, guild_id, guild_name, channel_id, channel_name}):
        raise ValueError('Expected at least one argument to be input.')

    conditions = []
    if not id == None:
        if isinstance(id, int):
            conditions.append(SellOrder.id == id)
        else:
            [conditions.append(SellOrder.id == d_id) for d_id in id]
    if not buy_order_id == None:
        if isinstance(buy_order_id, int):
            conditions.append(SellOrder.buy_order_id == buy_order_id)
        else:
            [conditions.append(SellOrder.buy_order_id == arg) for arg in buy_order_id]
    if not user_id == None:
        if isinstance(user_id, int):
            conditions.append(SellOrder.user_id == user_id)
        else:
            [conditions.append(SellOrder.user_id == arg) for arg in user_id]
    if not date_creation == None:
        if isinstance(date_creation, datetime):
            conditions.append(SellOrder.date_creation == date_creation)
        else:
            [conditions.append(SellOrder.date_creation == arg) for arg in date_creation]
    if not guild_id == None:
        if isinstance(guild_id, int):
            conditions.append(SellOrder.guild_id == guild_id)
        else:
            [conditions.append(SellOrder.guild_id == arg) for arg in guild_id]
    if not guild_name == None:
        if isinstance(guild_name, str):
            conditions.append(SellOrder.guild_name == guild_name)
        else:
            [conditions.append(SellOrder.guild_name == arg) for arg in guild_name]
    if not channel_id == None:
        if isinstance(channel_id, int):
            conditions.append(SellOrder.channel_id == channel_id)
        else:
            [conditions.append(SellOrder.channel_id == arg) for arg in channel_id]
    if not channel_name == None:
        if isinstance(channel_name, str):
            conditions.append(SellOrder.channel_name == channel_name)
        else:
            [conditions.append(SellOrder.channel_name == arg) for arg in channel_name]

    with (Session() if session == None else session) as local_session:
        sell_order = local_session.execute(select(SellOrder).where(*conditions)).all()
        if len(sell_order) == 1:
            yield sell_order[0][0]
        else: 
            yield sell_order[0]

        if session == None:
            local_session.commit()
        else:
            local_session.flush()

# TODO Move access request out of this function!
    # # Test if the requesting member us registered, or is there is NO users
    # if not user_is_registered(requesting_member) and not table_is_empty(User):
    #     raise error.ReqUserNotRegistered
    # # Check if the user is already registered
    # elif user_is_registered(member):
    #     raise error.UserAlreadyRegistired
def add_sell_order(user: User, buy_order: BuyOrder, ctx: commands.context.Context, items: List[Item], date_creation:datetime = datetime.now()) -> int:
    
    bo1 = SellOrder(date_creation = date_creation,
                    guild_id = ctx.guild.id,
                    guild_name = ctx.guild.name,
                    channel_id = ctx.channel.id,
                    channel_name = ctx.channel.name,
    
                    user = user,
                    items = items,
                    buy_order = buy_order
                    )
    session = Session.object_session(user)
    session.flush()

    return bo1.id

# TODO Move access request out of this function!
def add_user(member: discord.Member, priority: int=5, description: str="", alias = None) -> int:
    # Create User object
    user = User(name = member.display_name,
                priority = priority,
                disc = description,
                alias = alias,
                discord_id = member.id,
                discord_name = member.name,
                discord_discriminator = member.discriminator
                )
    
    user_id = None
    with Session() as session:
        session.add(user)
        session.flush()
        user_id = user.id
        session.commit()

    return user_id

@contextmanager
def get_user(session: Session = None,
             discord_id: Union[int, List[int]] = None,
             alias: Union[str, List[str]] = None,
             name: Union[str, List[str]] = None,
             discord_name: Union[str, List[str]] = None,
             discord_discriminator: Union[str, List[str]] = None,
             priority: int = None
             ) -> ContextManager[Union[User, List[User]]]:
    
    conditions = []
    
    # if all(v is None for v in {discord_id, alias, name, discord_name, discord_discriminator, priority}):
    #     raise ValueError('Expected at least one argument to be input.')

    if not discord_id == None:
        if isinstance(discord_id, int):
            conditions.append(User.discord_id == discord_id)
        else:
            [conditions.append(User.discord_id == d_id for d_id in discord_id)]
    if not alias == None:
        if isinstance(alias, str):
            conditions.append(User.alias == alias)
        else:
            [conditions.append(User.alias == arg) for arg in alias]
    if not name == None:
        if isinstance(name, str):
            conditions.append(User.name == name)
        else:
            [conditions.append(User.name == arg) for arg in name]
    if not discord_name == None:
        if isinstance(discord_name, str):
            conditions.append(User.discord_name == discord_name)
        else:
            [conditions.append(User.discord_name == arg) for arg in discord_name]
    if not discord_discriminator == None:
        if isinstance(discord_discriminator, str):
            conditions.append(User.discord_discriminator == discord_discriminator)
        else:
            [conditions.append(User.discord_discriminator == arg) for arg in discord_discriminator]
    if not priority == None:
        conditions.append(User.priority == priority)

    with (Session() if session == None else session) as local_session:
        user = local_session.execute(select(User).where(*conditions)).all()
        if len(user) == 1:
            yield user[0][0]
        else: 
            yield user[0]
            
        if session == None:
            local_session.commit()
        else:
            local_session.flush()
        
# TODO Move access request out of this function!
    # # Test if the requesting member us registered, or is there is NO users
    # if not user_is_registered(requesting_member):
    #     raise error.ReqUserNotRegistered
    # # Check if the user is already registered
    # elif not user_is_registered(requesting_member):
    #     raise error.UserIsNotRegistired
def delete_user(discord_member: Union[int, discord.Member]):
    with Session() as session:
        if isinstance(discord_member, discord.Member):
            statement = select(User).where(User.discord_id == discord_member.id)
        elif isinstance(discord_member, int):
            statement = select(User).where(User.discord_id == discord_member)

        user = session.execute(statement).one()[0]
        session.delete(user)
        session.commit()

def total_items_wanted(user: User) -> List[Item]:
    items = []
    for bo in user.buy_orders:
        for i1 in bo.items:
                for i2 in items:
                    if i1.type == i2.type:
                        i2.quantity = i2.quantity + i1.quantity
                    else:
                        items.append(Item(type=i1.type, quantity=i1.quantity))
    
    return items

def table_is_empty(table_class: Union[User, Item, SellOrder, BuyOrder]) -> bool:
    with Session() as session:
        if session.execute(select(table_class)).first():
            return False
        else:
            return True

def user_is_registered(session: Session = None,
                       discord_id: Union[int, List[int]] = None,
                       alias: Union[str, List[str]] = None,
                       name: Union[str, List[str]] = None,
                       discord_name: Union[str, List[str]] = None,
                       discord_discriminator: Union[str, List[str]] = None
                       ) -> bool:

    conditions = []
    if not discord_id == None:
        if isinstance(discord_id, int):
            conditions.append(User.discord_id == discord_id)
        else:
            [conditions.append(User.discord_id == d_id for d_id in discord_id)]
    if not alias == None:
        if isinstance(alias, str):
            conditions.append(User.alias == alias)
        else:
            [conditions.append(User.alias == arg) for arg in alias]
    if not name == None:
        if isinstance(name, str):
            conditions.append(User.name == name)
        else:
            [conditions.append(User.name == arg) for arg in name]
    if not discord_name == None:
        if isinstance(discord_name, str):
            conditions.append(User.discord_name == discord_name)
        else:
            [conditions.append(User.discord_name == arg) for arg in discord_name]
    if not discord_discriminator == None:
        if isinstance(discord_discriminator, str):
            conditions.append(User.discord_discriminator == discord_discriminator)
        else:
            [conditions.append(User.discord_discriminator == arg) for arg in discord_discriminator]

    subq = exists().where(*conditions)

    with (Session() if session == None else session) as local_session:
        # res = local_session.execute(select(User.id).where(subq)).first()
        if local_session.execute(select(User.id).where(subq)).first():
            return True
        else:
            return False

def early_test_main():
    user = User(name='Neorim', 
        priority=2, 
        disc='test disc', 
        alias='neo', 
        discord_id=922337203685477580, 
        discord_name='Neorim',
        discord_discriminator='Neorim#0099')

    with Session() as session:
        subq = exists().where(User.discord_id == user.discord_id)
        if not session.execute(select(User.id).where(~subq)).first():
            session.add(user)
            session.commit()
    
    with Session() as session:
        u2 = session.execute(select(User).where(User.name == 'Neorim')).first()

    _ = input('Press for next step\n')

    with Session() as session:
        results = session.execute(select(User).where(User.name == 'Neorim'))
        users = results.scalars().all()
        for user in users:
            session.delete(user)
            session.commit()