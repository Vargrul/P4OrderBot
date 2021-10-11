import re
import discord
import copy
from discord.channel import CategoryChannel
import orderbot.src.errors as errors
from orderbot.src.database_ctrl import Item, User
from orderbot.src.order import Order

from orderbot.src.global_data import P4_ITEM_ALIAS
from typing import List, Tuple
import pickle
from discord import Guild, TextChannel


__orders: Tuple[Order] = []

def get_orders(guild: Guild=None, channel: TextChannel=None, user: User=None) -> List[Order]:
    # Get list of all orders
    return_orders = __orders
    
    # Begin to filter the results down depending on the input to the function
    if guild != None:
        return_orders = [o for o in return_orders if o.guild_id == guild.id]

    if channel != None:
        return_orders = [o for o in return_orders if o.channel_id == channel.id]

    if user != None:
        return_orders = [o for o in return_orders if o.user.id == user.id]

    return return_orders

def add_order(order: Order):
    __orders.append(order)
    save_orders()
    pass

def user_total_orders_to_discord_string(user: User, guild: Guild=None, channel: TextChannel=None) -> str:
    user_orders = get_orders(guild = guild, channel = channel, user = user)

    response = (
        f'Issuer: **{user.name}** Alias: **{user.alias}**\n'
        f'User ID: **{user.id}**\n')

    if len(user_orders) == 0:
        response = response + f" __***None***__"
    else:
        # Need copy of items to not change the orders
        items = [copy.copy(i) for i in user_orders[0].items]
        if len(user_orders) > 1:
            for o in user_orders[1:]:
                for idx, i in enumerate(items):
                    for oi in o.items:
                        if i.name == oi.name:
                            items[idx].count = items[idx].count + oi.count
                            break
        
        
        response = response + f'```css\n'
        for i in items:
            response = response + (f'{i.count:7} - {i.name:25}\n')
        response = response + f'```'

    return response

# TODO Going to be obsolete
def add_order_from_items(user: User, items: List[Item], guild: Guild, channel: TextChannel) -> Order:
    order = Order(user, items, guild_id=guild.id, guild_name=guild.name, channel_id=channel.id, channel_name=channel.name)
    add_order(order)
    return order

# TODO Going to be obsolete
def add_order_from_lists(user: User, name_lst: List[str], count_lst: List[int], guild: Guild, channel: TextChannel) -> Order:
    # add items not in order for completeness
    for i_n in P4_ITEM_ALIAS:
        if not any(e in i_n for e in name_lst):
            name_lst.append(i_n[0])
            count_lst.append(0)
    
    # change names to full names
    for i_n in P4_ITEM_ALIAS:
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
    for i_name in [i[0] for i in P4_ITEM_ALIAS]:
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
                if in_item.name == order_item.name and order_item.count != 0:
                    if in_item.count == None:
                        if order_item not in items_filled:
                            items_filled.append(Item(order_item.name, order_item.count))
                        else:
                            item = [item for item in items_filled if item.name == order_item.name][0]
                            item.count = item.count + order_item.count

                        # Set in_item to 0 to show is was filled
                        __orders[io].items[i].count = 0
                        break

                    if in_item.count <= order_item.count and in_item.count != 0:
                        items_filled.append(Item(order_item.name, order_item.count))

                        __orders[io].items[i].count = __orders[io].items[i].count - in_items[in_i].count
                        in_items[in_i].count = 0
                        break


    # Set all None types(complete fill) to 0 as everything possible have been filled.
    for i in in_items:
        if i.count == None:
            i = 0


    # delete filled orders
    orders_to_delete = []
    for i, order in enumerate(__orders):
        if not any([x.count for x in order.items]):
            orders_to_delete.append(i)
    
    orders_to_delete.sort(reverse=True)
    for del_nr in orders_to_delete:
        del __orders[del_nr]
        
    save_orders()

    # Check if order was fille, if so -> remove order. (pm issuer?)
    return items_filled

# TODO Going to be obsolete
def fill_order_from_lists( user: User, name_lst: List[str], count_lst: List[int]) -> Tuple[Item]:
    # REPEATED CODE! Should be in another funciton (same as add_order_from_lists())
    for i_n in P4_ITEM_ALIAS:
        if not any(e in i_n for e in name_lst):
            name_lst.append(i_n[0])
            count_lst.append(0)
    
    # change names to full names
    for i_n in P4_ITEM_ALIAS:
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