from sqlalchemy.orm import with_expression
import pytest
import discord

from sqlalchemy import select, exists

import orderbot.src.database_ctrl as database_ctrl
from orderbot.src.database_ctrl import User

test_data = [
    (42, True),
    (69, False)
]
@pytest.mark.parametrize("disc_member_id, expected", test_data)
def test_user_is_registered(discord_member_clean, disc_member_id, expected, prep_db_add_test_user):
    discord_member_clean.id = disc_member_id
    assert database_ctrl.user_is_registered(discord_id = discord_member_clean.id) == expected


def test_table_is_empty_empty():
    assert database_ctrl.table_is_empty(User) == True


def test_table_is_empty_not_empty(prep_db_add_test_user):
    assert database_ctrl.table_is_empty(User) == False

def test_add_user_empty_db(mocker, clean_db):
    member = mocker.Mock(spec=discord.Member)
    member.display_name = 'TestUser1 Disp'
    member.id = 123654789
    member.name = 'TestUser1'
    member.discriminator = 'TestUser1#0001',

    requesting_member = mocker.Mock(spec=discord.Member)
    requesting_member.display_name = 'ReqUserNotReged Disp'
    requesting_member.id = 147852369
    requesting_member.name = 'ReqUserNotReged'
    requesting_member.discriminator = 'ReqUserNotReged#0000'
    
    try:
        database_ctrl.add_user(member, requesting_member)
    except:
        pass

    with database_ctrl.Session() as session:
        subq = exists().where(User.discord_id == member.id)
        res = session.execute(select(User.discord_id).where(subq)).first()
        assert bool(res)

def test_add_user(add_user_data_fixture, prep_db_add_test_user):
    member, requesting_member, priority, description, alias, expected = add_user_data_fixture
    try:
        database_ctrl.add_user(member, requesting_member, priority, description, alias)
    except:
        pass
    
    # Verify
    with database_ctrl.Session() as session:
        subq = exists().where(User.discord_id == member.id)
        res = session.execute(select(User.discord_id).where(subq)).first()
        assert bool(res) == expected

def test_get_user(prep_db_add_test_user):
    with database_ctrl.get_user(discord_id = 42) as user:
        assert user.name == "Test" and user.discord_id == 42

def test_delete_user_int(prep_db_add_test_user):
    database_ctrl.delete_user(42, 42)

    # Verify
    with database_ctrl.Session() as session:
        subq = exists().where(User.discord_id == 42)
        res = session.execute(select(User.discord_id).where(subq)).first()
        assert bool(res) == False

def test_delete_user_member(mocker, prep_db_add_test_user):
    d1 = mocker.Mock(spec=discord.Member)
    d1.id = 42

    database_ctrl.delete_user(d1, d1)

    # Verify
    with database_ctrl.Session() as session:
        subq = exists().where(User.discord_id == d1.id)
        res = session.execute(select(User.discord_id).where(subq)).first()
        assert bool(res) == False        