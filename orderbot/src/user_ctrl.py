import discord
from discord import user
from orderbot.src.database_ctrl import User
import orderbot.src.errors as error
from typing import List
import pickle

# Variables
users: List[User] = None

# Functions
def save_users() -> None:
    with open('orderbot/data/users.pckl', 'wb') as file:
        pickle.dump(users, file, pickle.HIGHEST_PROTOCOL)

def load_users() -> None:
    try:
        with open('orderbot/data/users.pckl', 'rb') as file:
            global users
            users = pickle.load(file)
    except:
        return

def add_user(member: discord.Member, requesting_member: discord.Member, priority: int=5, discription: str="", alias = None) -> None:
    if not user_is_registered(requesting_member) and len(users) != 0:
        raise error.ReqUserNotRegistered
    elif user_is_registered(member):
        raise error.UserAlreadyRegistired

    users.append(User(member.display_name, priority, alias=alias, disc = discription, discord_id=member.id, discord_name=member.name, discord_discriminator=member.discriminator))
    save_users()


def remove_user(member: discord.Member, requesting_member: discord.Member) -> None:
    if not user_is_registered(requesting_member):
        raise error.ReqUserNotRegistered
    elif not user_is_registered(member):
        raise error.UserIsNotRegistired

    for i, u in enumerate(users):
        if u.discord_id == member.id:
            del users[i]
            save_users()

# TODO Make these functions in to one
def get_user_by_alias(alias: str) -> User:
    for user in users:
        if user.alias.lower() == alias.lower():
            return user

def get_user_by_id(user_id: int) -> User:
    for user in users:
        if user.id == user_id:
            return user

def get_user_from_member(member: discord.Member) -> User:
    return next(u for u in users if u.discord_id == member.id)

def user_is_registered(member: discord.Member) -> bool:
    for user in users:
        if member.id == user.discord_id:
            return True
    return False

# Module Init
load_users()