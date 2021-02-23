import discord
from discord import user
from orderbot.src.user import User
import orderbot.src.errors as error
from typing import List
import pickle

class UserCtrl:
    def __init__(self, users: List[User] = []) -> None:
        self.users: List[User] = users

    def save_users(self) -> None:
        with open('orderbot/data/users.pckl', 'wb') as file:
            pickle.dump(self.users, file, pickle.HIGHEST_PROTOCOL)

    def load_users(self) -> None:
        try:
            with open('orderbot/data/users.pckl', 'rb') as file:
                self.users = pickle.load(file)
        except:
            return

    def add_user(self, member: discord.Member, requesting_member: discord.Member, priority: int=5, discription: str="", alias = None) -> None:
        if not self.user_is_registered(requesting_member) and len(self.users) != 0:
            raise error.ReqUserNotRegistered
        elif self.user_is_registered(member):
            raise error.UserAlreadyRegistired

        self.users.append(User(member.display_name, priority, alias=alias, disc = discription, discord_id=member.id, discord_name=member.name, discord_discriminator=member.discriminator))
        self.save_users()


    def remove_user(self, member: discord.Member, requesting_member: discord.Member) -> None:
        if not self.user_is_registered(requesting_member):
            raise error.ReqUserNotRegistered
        elif not self.user_is_registered(member):
            raise error.UserIsNotRegistired

        for i, u in enumerate(self.users):
            if u.discord_id == member.id:
                del self.users[i]
                self.save_users()

    # TODO Make these functions in to one
    def get_user_by_alias(self, alias: str) -> User:
        for user in self.users:
            if user.alias == alias:
                return user
    
    def get_user_by_id(self, user_id: int) -> User:
        for user in self.users:
            if user.id == user_id:
                return user

    def get_user_from_member(self, member: discord.Member) -> User:
        return next(u for u in self.users if u.discord_id == member.id)

    def user_is_registered(self, member: discord.Member) -> bool:
        for user in self.users:
            if member.id == user.discord_id:
                return True

        return False