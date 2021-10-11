import pickle
from enum import Enum, auto


class FILL_INPUT_TYPE(Enum):
    ID_AND_LINK = auto()
    ID_AND_SHORTHAND = auto()
    ID_AND_P4TYPE = auto()
    ONLY_LINK = auto()
    ONLY_SHORTHAND = auto()
    ONLY_P4TYPE = auto()

class StatusEnum(Enum):
    OPEN = 1
    CLOSED = 2
    ALMOST_FILLED = 3

class P4ItemEnum(Enum):
    BCN = 1
    IRD = 2
    NF = 3
    OMA = 4
    RCM = 5
    SHPC = 6
    SC = 7
    WM = 8

P4_ITEM_ALIAS = {
    P4ItemEnum.BCN: ['Broadcast Node', 'BCN'],
    P4ItemEnum.IRD: ['Integrity Response Drones', 'IRD'],
    P4ItemEnum.NF: ['Nano-Factory', 'NF'],
    P4ItemEnum.OMA: ['Organic Mortar Applicators', 'OMA'],
    P4ItemEnum.RCM: ['Recursive Computing Module', 'RCM'],
    P4ItemEnum.SHPC: ['Self-Harmonizing Power Core', 'SHPC'],
    P4ItemEnum.SC: ['Sterile Conduits', 'SC'],
    P4ItemEnum.WM: ['Wetware Mainframe', 'WM']
}

order_id_counter = 0
user_id_counter = 0

def get_new_order_id():
    global order_id_counter
    order_id_counter = order_id_counter + 1
    save_nonstatic_globals()
    return order_id_counter

def get_new_user_id():
    global user_id_counter
    user_id_counter = user_id_counter + 1
    save_nonstatic_globals()
    return user_id_counter

def save_nonstatic_globals():
    global order_id_counter
    global user_id_counter
    variable = [order_id_counter, user_id_counter]
    try:
        with open('orderbot/data/misc_data.pckl', 'wb') as f:
            pickle.dump(variable, f, pickle.HIGHEST_PROTOCOL)
    except:
        return

def load_nonstatic_globals():
    try:
        with open('orderbot/data/misc_data.pckl', 'rb') as f:
            variables = pickle.load(f)
    except:
        return
    global order_id_counter
    global user_id_counter
    order_id_counter = variables[0]
    user_id_counter = variables[1]
    pass