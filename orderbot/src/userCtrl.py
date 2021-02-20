from orderbot.src.user import User
import orderbot.src.errors as error
from typing import List
import pickle

class UserCtrl:
    def __init__(self, users: List[User] = []) -> None:
        self.users = users

    def save_users(self) -> None:
        user_dict = [[u.name, u.priority, u.alias, u.disc, u.id] for u in self.users]
        with open('orderbot/data/users.pckl', 'wb') as file:
            pickle.dump(user_dict, file, pickle.HIGHEST_PROTOCOL)

    def load_users(self) -> None:
        user_dict = []
        try:
            with open('orderbot/data/users.pckl', 'rb') as file:
                user_dict = pickle.load(file)
        except:
            return

        users = []
        for ud in user_dict:
            users.append(User(*ud))
        
        self.users = users

    def add_user(self, user_name: str, requesting_user_name: str, priority: int=5, discription: str="", alias = None) -> None:
        if not self.user_is_registered(requesting_user_name) and len(self.users) != 0:
            raise error.ReqUserNotRegistered
        elif self.user_is_registered(user_name):
            raise error.UserAlreadyRegistired

        self.users.append(User(user_name, priority, alias=alias, disc = discription, ))
        self.save_users()


    def remove_user(self, user_name: str, requesting_user_name: str) -> None:
        if not self.user_is_registered(requesting_user_name):
            raise error.ReqUserNotRegistered
        elif not self.user_is_registered(user_name):
            raise error.UserIsNotRegistired

        for i, u in enumerate(self.users):
            if u.name == user_name:
                del self.users[i]
                self.save_users()

    def get_user_by_name(self, user_name: str) -> User:
        for user in self.users:
            if user.name == user_name:
                return user

    def user_is_registered(self, user_name: str) -> bool:
        for user in self.users:
            if user_name == user.name:
                return True

        return False