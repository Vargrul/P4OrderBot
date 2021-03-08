from typing import List
from orderbot.src.item import Item


class UserError(Exception):
    pass

class ReqUserNotRegistered(UserError):
    pass

class UserAlreadyRegistired(UserError):
    pass

class UserIsNotRegistired(UserError):
    pass


class OrderError(Exception):
    pass

class OrderNonAvailableError(Exception):
    pass

class OrderInputError(Exception):
    pass

class OrderMoreThanOneError(Exception):
    pass

class OrderShorthandInputError(Exception):
    pass

class IdentifierError(Exception):
    pass

class ItemOverFillError(Exception):
    def __init__(self, item):
        self.item: List[Item] = item

class ItemNotNeededError(Exception):
    def __init__(self, item):
        self.item: List[Item] = item