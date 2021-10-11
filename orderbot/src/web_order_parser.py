from orderbot.src.global_data import get_new_user_id
import requests
from html.parser import HTMLParser
import numpy as np
from typing import Tuple

import orderbot.src.order as Order

class OrderHtmlParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.str_order: str = None
        self.order = None


    def handle_starttag(self, tag, attrs):
        if tag == 'meta':
            if ('name', 'description') in attrs:
                self.str_order = [l[1] for l in attrs if l[0] == 'content'][0]

    def convert_to_lsts(self):
        temp = [l.split(' - ') for l in self.str_order.splitlines()]
        name = [row[0] for row in temp]
        count = [int(row[1]) for row in temp]
        
        return name, count

def get_lsts_from_web_order(web_order_addr) -> Tuple[str, int]:
    req = requests.get(web_order_addr)
    orderHtmlParser = OrderHtmlParser()
    orderHtmlParser.feed(req.text)

    return orderHtmlParser.convert_to_lsts()
