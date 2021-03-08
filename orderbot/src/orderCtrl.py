import discord
import orderbot.src.errors as errors
from orderbot.src.item import Item
from orderbot.src.order import Order
from orderbot.src.user import User
from orderbot.src.global_data import P4_ITEM_NAMES
from typing import List, Tuple
import pickle
from discord import Guild, TextChannel


__orders: Tuple[Order] = []

def get_orders(guild: Guild=None, channel: TextChannel=None) -> List[Order]:
    if guild != None:
        if channel != None:
            return [o for o in __orders if o.channel_id == channel.id and o.guild_id == guild.id]
        else:
            return [o for o in __orders if o.guild_id == guild.id]

    return __orders

def add_order(order: Order):
    __orders.append(order)
    save_orders()
    pass

# TODO Going to be obsolete
def add_order_from_items(user: User, items: List[Item], guild: Guild, channel: TextChannel) -> Order:
    order = Order(user, items, guild_id=guild.id, guild_name=guild.name, channel_id=channel.id, channel_name=channel.name)
    add_order(order)
    return order

# TODO Going to be obsolete
def add_order_from_lists(user: User, name_lst: List[str], count_lst: List[int], guild: Guild, channel: TextChannel) -> Order:
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
        
    return add_order_from_items(user, items, guild, channel)

# TODO Add error handling for order not existing in list.
def delete_order( order_id):
    for i, o in enumerate(__orders):
        if o.id == order_id:
            del __orders[i]
    
    save_orders()

# Gives error if not needed
# - (Secondary) Take Partial??
# First in -> First out
# TODO Going to refactored to using Order as input
def fill_order( user: User, in_items: List[Item]) -> Tuple[Item]:
    # get orders from user
    items_filled = []
    order_nrs = []
    for i, o in enumerate(__orders):
        if o.user == user:
            order_nrs.append(i)

    # Concatenate all orders for the user for a Total needed list
    needed_items_list: List[Item] = []
    for i_name in [i[0] for i in P4_ITEM_NAMES]:
        count = 0
        for io in order_nrs:
            for i, order_item in enumerate(__orders[io].items):
                if order_item.name == i_name:
                    count = count + order_item.count
                    break
        needed_items_list.append(Item(i_name, count))
    
    # Error checking
    item_overfill = []
    item_not_needed = []
    for n_item in needed_items_list:
        for i_item in in_items:
            if n_item.name == i_item.name:
                if(i_item.count == None and n_item.count == 0) or (i_item.count != 0 and n_item.count == 0):
                    item_not_needed.append(i_item)
                elif i_item.count != None:
                    if i_item.count > n_item.count:
                        item_overfill.append(i_item)

                break

    if len(item_overfill) != 0:
        raise errors.ItemOverFillError(item_overfill)
    if len(item_not_needed) != 0:
        raise errors.ItemNotNeededError(item_not_needed)           

    # Fill orders
    for io in order_nrs:
        for i, order_item in enumerate(__orders[io].items):
            for in_i, in_item in enumerate(in_items):
                if in_item.name == order_item.name:
                    if in_item.count == None and order_item.count != 0:
                        items_filled.append(Item(order_item.name, order_item.count))

                        # Set in_item to 0 to show is was filled
                        in_items[in_i].count = 0
                        # Set order_item to 0 as it was filled completely
                        __orders[io].items[i].count = 0

                    if in_item.count <= order_item.count and in_item.count != 0:
                        items_filled.append(Item(order_item.name, order_item.count))

                        __orders[io].items[i].count = __orders[io].items[i].count - in_items[in_i].count
                        in_items[in_i].count = 0

                    break


    # delete filled orders
    orders_to_delete = []
    for i, order in enumerate(__orders):
        if not any([x.count for x in order.items]):
            orders_to_delete.append(i)
    
    orders_to_delete.reverse()
    for del_nr in orders_to_delete:
        del __orders[del_nr]

    # Does ONLY fill if the in items are <= the order_items
    # must be able to do this better -.-
    # for io in order_nrs:
    #     for i, order_item in enumerate(__orders[io].items):
    #         for in_i, in_item in enumerate(in_items):
    #             if in_item.name == order_item.name:
    #                 if in_item.count == None and order_item.count != 0:
    #                     items_filled.append(Item(order_item.name, order_item.count))

    #                     # Set in_item to 0 to show is was filled
    #                     in_items[in_i].count = 0
    #                     # Set order_item to 0 as it was filled completely
    #                     __orders[io].items[i].count = 0

    #                 elif (in_item.count == None and order_item.count == 0) \
    #                     or (in_item.count != 0 and order_item.count == 0):
    #                     item_not_needed.append(in_item)

    #                 elif in_item.count <= order_item.count and in_item.count != 0:
    #                     items_filled.append(Item(order_item.name, order_item.count))

    #                     __orders[io].items[i].count = __orders[io].items[i].count - in_items[in_i].count
    #                     in_items[in_i].count = 0

    #                 elif in_item.count > order_item.count:
    #                     item_overfill.append(in_item)

    #                 break

    #                 # elif in_item.count < order_item.count:
    #                 #     __orders[io].items[i].count = __orders[io].items[i].count - in_items[in_i].count
    #                 #     in_items[in_i].count = 0
    #                 # else:
    #                 #     in_items[in_i].count = in_items[in_i].count - __orders[io].items[i].count
    #                 #     __orders[io].items[i].count = 0
    #                 # break

    # orders_to_delete = []
    # for i, order in enumerate(__orders):
    #     if not any([x.count for x in order.items]):
    #         orders_to_delete.append(i)
    
    # orders_to_delete.reverse()
    # for del_nr in orders_to_delete:
    #     del __orders[del_nr]
        
    save_orders()

    # Check if order was fille, if so -> remove order. (pm issuer?)
    return items_filled

# TODO Going to be obsolete
def fill_order_from_lists( user: User, name_lst: List[str], count_lst: List[int]) -> Tuple[Item]:
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

    return fill_order(user, items)

def create_order_from_lists(user: User, name_lst: List[str], count_lst: List[int], guild: Guild, channel: TextChannel):
    return Order(user, )

def check_order_id( id: int, guild: Guild = None, channel: TextChannel = None) -> bool:
    for o in get_orders(guild, channel):
        if o.id == id:
            return True
    return False

def save_orders():
    try:
        with open('orderbot/data/orders.pckl', 'wb') as file:
            pickle.dump(__orders, file, pickle.HIGHEST_PROTOCOL)
    except:
        return

def load_orders():
    try:
        with open('orderbot/data/orders.pckl', 'rb') as file:
            global __orders
            __orders = pickle.load(file)
    except:
        return

# Module Init Code
load_orders()