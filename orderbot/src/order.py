from datetime import datetime
from orderbot.src.user import User
from orderbot.src.item import Item
import orderbot.src.global_data as global_data
from typing import List

class Order:
    def __init__(self, user: User, items: List[Item] = None, date: datetime = datetime.now(), id: int = None, guild_id: int = None, guild_name: str = None, channel_id: int = None, channel_name: str = None):
        self.user: User = user
        self.items: List[Item] = items
        self.date: datetime = date
        if id is None:
            self.id: int = global_data.get_new_order_id()
        else:
            self.id: int = id

        self.guild_id: int = guild_id
        self.guild_name: str = guild_name
        self.channel_id: int = channel_id
        self.channel_name: str = channel_name

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