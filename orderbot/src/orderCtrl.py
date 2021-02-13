from orderbot.src.item import Item
from orderbot.src.order import Order
from orderbot.src.user import User
from orderbot.src.userCtrl import UserCtrl
from orderbot.src.global_data import P4_ITEM_NAMES
import orderbot.src.errors as errors
from typing import List
import pickle

class OrderCtrl:
    
    def __init__(self):
        self.orders = []
    
    @property
    def orders(self):
        return self.__orders

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

    def add_order_from_items(self, user: User, items: List[Item]):
        order = Order(user, items)
        self.add_order(order)

    def add_order_from_lists(self, user: str, user_ctrl: UserCtrl, name_lst: List[str], count_lst: List[int]):
        if not user_ctrl.user_is_registered(user):
            raise errors.ReqUserNotRegistered

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
            
        self.add_order_from_items(user, items)
        pass

    # TODO Add error handling for order not existing in list.
    def delete_order(self, order_id):
        for i, o in enumerate(self.orders):
            if o.id == order_id:
                del self.orders[i]
        
        self.save_orders()

    # Gives error if not needed
    # - (Secondary) Take Partial??
    # First in -> First out
    def fill_order(self, target_user: str, in_items: List[Item]):
        # get orders from user
        order_nrs = []
        for i, o in enumerate(self.orders):
            if o.user_name == target_user:
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

    def fill_order_from_lists(self, user: str, name_lst: List[str], count_lst: List[int]):
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

    def save_orders(self):
        order_dict = []
        for o in self.__orders:
            tmp_dict = [o.user_name, o.date, o.id]
            tmp_dict.append([[i.count, i.name, i.alias] for i in o.items])
            order_dict.append(tmp_dict)
        # order_dict = [[o.user, o.date, o.items] for o in self.__orders]
        try:
            with open('orderbot/data/orders.pckl', 'wb') as file:
                pickle.dump(order_dict, file, pickle.HIGHEST_PROTOCOL)
        except:
            return

    def load_orders(self):
        order_dict = []
        try:
            with open('orderbot/data/orders.pckl', 'rb') as file:
                order_dict = pickle.load(file)
        except:
            return
        orders = []
        for od in order_dict:
            items = []
            for id in od[3]:
                items.append(Item(id[1], id[0], id[2]))
            orders.append(Order(od[0], items, date = od[1], id = od[2]))
        
        self.__orders = orders
