import orderbot.src.global_data as global_data

class User:
    def __init__(self, name: str, prioity: int, alias: str="", disc: str="", id: int=None) -> None:
        self.name = name
        self.priority = prioity
        self.disc = disc
        self.alias = alias
        if id is None:
            self.id = global_data.get_new_user_id()
        else:
            self.id = id