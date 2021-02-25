import discord
from discord import errors
from orderbot.src.item import Item
from orderbot.src.order import Order
from orderbot.src.user import User
from orderbot.src.userCtrl import UserCtrl
from orderbot.src.global_data import P4_ITEM_NAMES
# import orderbot.src.errors as errors
from typing import List, Tuple
import pickle
from discord import Guild, TextChannel

class OrderCtrl:
    
    def __init__(self):
        self.orders: Tuple[Order] = []

    def get_orders(self, guild: Guild=None, channel: TextChannel=None) -> List[Order]:
        if guild != None:
            if channel != None:
                return [o for o in self.__orders if o.channel_id == channel.id and o.guild_id == guild.id]
            else:
                return [o for o in self.__orders if o.guild_id == guild.id]

        return self.__orders

    orders = property(get_orders)

    @orders.setter
    def orders(self, orders: List[Order]):
        self.__orders = orders

    def __str__(self) -> str:
        return '\n'.join(str(o) for o in self.orders)

    def get_pretty_str(self):
        pass

    def add_order(self, order: Order):
        self.__orders.append(order)
        self.save_orders()
        pass

    def add_order_from_items(self, user: User, items: List[Item], guild: Guild, channel: TextChannel) -> Order:
        order = Order(user, items, guild_id=guild.id, guild_name=guild.name, channel_id=channel.id, channel_name=channel.name)
        self.add_order(order)
        return order

    def add_order_from_lists(self, user: User, name_lst: List[str], count_lst: List[int], guild: Guild, channel: TextChannel) -> Order:
        # add items not in order for completeness
        for i_n in P4_ITEM_NAMES:
            if not any(e in i_n for e in name_lst):
                name_lst.append(i_n[0])
                count_lst.append(0)
        
        # change names to full names
        for i_n in P4_ITEM_NAMES:
            for i, name in enumerate(name_lst):
                if name in i_n:
                    name_lst[i] = i_n[0]

        item_in_lst = sorted(zip(name_lst, count_lst), key=lambda e: e[0])

        items = []
        for name, count in item_in_lst:
            items.append(Item(name, count))
            
        return self.add_order_from_items(user, items, guild, channel)

    # TODO Add error handling for order not existing in list.
    def delete_order(self, order_id):
        for i, o in enumerate(self.orders):
            if o.id == order_id:
                del self.orders[i]
        
        self.save_orders()

    # Gives error if not needed
    # - (Secondary) Take Partial??
    # First in -> First out
    def fill_order(self, user: User, in_items: List[Item]):
        # get orders from user
        order_nrs = []
        for i, o in enumerate(self.orders):
            if o.user == user:
                order_nrs.append(i)

        # must be able to do this better -.-
        for io in order_nrs:
            for i, order_item in enumerate(self.orders[io].items):
                for in_i, in_item in enumerate(in_items):
                    if in_item.name == order_item.name:
                        if in_item.count < order_item.count:
                            self.orders[io].items[i].count = self.orders[io].items[i].count - in_items[in_i].count
                            in_items[in_i].count = 0
                        else:
                            in_items[in_i].count = in_items[in_i].count - self.orders[io].items[i].count
                            self.orders[io].items[i].count = 0
                        break

        orders_to_delete = []
        for i, order in enumerate(self.orders):
            if not any([x.count for x in order.items]):
                orders_to_delete.append(i)
        
        orders_to_delete.reverse()
        for del_nr in orders_to_delete:
            del self.orders[del_nr]
            
        self.save_orders()

        # Check if order was fille, if so -> remove order. (pm issuer?)
        pass

    def fill_order_from_lists(self, user: User, name_lst: List[str], count_lst: List[int]):
        # REPEATED CODE! Should be in another funciton (same as add_order_from_lists())
        for i_n in P4_ITEM_NAMES:
            if not any(e in i_n for e in name_lst):
                name_lst.append(i_n[0])
                count_lst.append(0)
        
        # change names to full names
        for i_n in P4_ITEM_NAMES:
            for i, name in enumerate(name_lst):
                if name in i_n:
                    name_lst[i] = i_n[0]

        item_in_lst = sorted(zip(name_lst, count_lst), key=lambda e: e[0])

        items = []
        for name, count in item_in_lst:
            items.append(Item(name, count))

        self.fill_order(user, items)

    def check_order_id(self, id: int, guild: Guild = None, channel: TextChannel = None) -> bool:
        for o in self.get_orders(guild, channel):
            if o.id == id:
                return True
        return False

    def save_orders(self):
        try:
            with open('orderbot/data/orders.pckl', 'wb') as file:
                pickle.dump(self.__orders, file, pickle.HIGHEST_PROTOCOL)
        except:
            return

    def load_orders(self):
        try:
            with open('orderbot/data/orders.pckl', 'rb') as file:
                self.__orders = pickle.load(file)
        except:
            return
