from datetime import datetime
from orderbot.src.user import User
from orderbot.src.item import Item
import orderbot.src.global_data as global_data
from typing import List

class Order:
    def __init__(self, user_name: User, items: List[Item] = None, date: datetime = datetime.now(), id = None):
        self.user_name = user_name
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

    def __str__(self) -> str:
        retStr = self.user_name + '\n\t' + '\n\t'.join(str(i) for i in self.items)
        return retStr