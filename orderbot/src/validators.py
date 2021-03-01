import re
from typing import List, Pattern, Tuple

def valid_link(url: str):
    # validate web page test
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return regex.search(url)

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

def extract_shorthand_p4(shorthand: str) -> Tuple[List[str], List[int]]:
    regex = get_shorthand_regex(shorthand)
    res = regex.findall(shorthand)

    shorthand = shorthand.strip()
    if shorthand[0].isdigit():
        str_lst = [s[1] for s in res]
        int_lst = [int(s[0]) for s in res]
    else:
        str_lst = [s[0] for s in res]
        int_lst = [int(s[1]) for s in res]
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