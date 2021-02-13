import pickle

P4_ITEM_NAMES = [
    ['Broadcast Node', 'BCN'],
    ['Integrity Response Drones', 'IRD'],
    ['Nano-Factory', 'NF'],
    ['Organic Mortar Applicators', 'OMA'],
    ['Recursive Computing Module', 'RCM'],
    ['Self-Harmonizing Power Core', 'SHPC'],
    ['Sterile Conduits', 'SC'],
    ['Wetware Mainframe', 'WM']
    ]
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