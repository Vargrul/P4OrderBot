import re
from typing import List, Pattern, Tuple

import orderbot.src.regexes as regexes
from orderbot.src.database_ctrl import Item

def valid_id_and_link(arg: str):
    regex = regexes.regex_id_and_link()
    return regex.search(arg)

def valid_link(arg: str):
    regex = regexes.regex_link_only()    
    return regex.search(arg)

def valid_id_and_shorthand(arg: str):
    regex = regexes.regex_id_and_shorthand()
    return regex.search(arg)

def valid_shorthand(arg: str):
    regex = regexes.regex_shorthand_only()
    return regex.search(arg)

def valid_id_and_p4type(arg: str):
    regex = regexes.regex_id_and_p4type()
    return regex.search(arg)

def valid_p4type(arg: str):
    regex = regexes.regex_p4types_only()
    return regex.search(arg)

# TODO fix this - Should not be needed
def get_shorthand_regex(shorthand: str) -> Pattern:
    shorthand = shorthand.strip()
    if shorthand[0].isdigit():
        regex = re.compile(
            r'(\d+)\s*(\bSC\b|\bNF\b|\bIRD\b|\bOMA\b|\bBCN\b|\bSHPC\b|\bRCM\b|\bWM\b)\s*'
            )
    else:
        regex = re.compile(
            r'(\bSC\b|\bNF\b|\bIRD\b|\bOMA\b|\bBCN\b|\bSHPC\b|\bRCM\b|\bWM\b)\s*(\d+)\s*'
            )
    return regex

def valid_shorthand_p4(shorthand: str) -> bool:
    regex = get_shorthand_regex(shorthand)
    
    if len(regex.sub('', shorthand).strip()) == 0:
        return True
    else:
        return False

def extract_shorthand_p4(shorthand: str) -> List[Item]:
    regex = get_shorthand_regex(shorthand)
    res = regex.findall(shorthand)

    shorthand = shorthand.strip()
    if shorthand[0].isdigit():
        str_lst = [s[1] for s in res]
        int_lst = [int(s[0]) for s in res]
    else:
        str_lst = [s[0] for s in res]
        int_lst = [int(s[1]) for s in res]
    
    # Convert to Items
    return str_lst, int_lst

def extract_invalid_part_shorthand_p4(shorthand: str) -> str:
    regex = get_shorthand_regex(shorthand)
    return regex.sub('', shorthand).strip()

def any_part_valid_shorthand_p4(shorthand: str) -> bool:
    shorthand = shorthand.strip()
    if len(extract_invalid_part_shorthand_p4(shorthand)) < len(shorthand):
        return True
    else:
        return False
        