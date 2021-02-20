
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

class IdentifierError(Exception):
    pass