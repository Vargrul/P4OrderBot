from datetime import datetime
from orderbot.src.user import User
from orderbot.src.userCtrl import UserCtrl
from orderbot.src.item import Item
import orderbot.src.global_data as global_data
from typing import List

class Order:
    def __init__(self, user: User, items: List[Item] = None, date: datetime = datetime.now(), id = None):
        self.user = user
        self.items = items
        self.date = date
        if id is None:
            self.id = global_data.get_new_order_id()
        else:
            self.id = id

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item_name):
        for i, it in enumerate(self.items):
            if it.name == item_name:
                del self.items[i]

    def to_discord_string(self) -> str:
        response = (
            f'Issuer: **{self.user.name}** Alias: **{self.user.alias}**\n'
            f'Order ID: **{self.id}**\n```css\n'
            )
        for item in self.items:
            response = response + (f'{item.count:7} - {item.name:25}\n')
        response = response + f'```'
        return response

    def __str__(self) -> str:
        retStr = self.user.name + '\n\t' + '\n\t'.join(str(i) for i in self.items)
        return retStr