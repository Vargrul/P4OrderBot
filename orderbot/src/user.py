import orderbot.src.global_data as global_data

class User:
    def __init__(self, name: str, prioity: int, alias: str="", disc: str="", id: int=None, discord_id: int= None, discord_name: str=None, discord_discriminator: int=None) -> None:
        self.name = name
        self.priority = prioity
        self.disc = disc
        self.alias = alias
        if id is None:
            self.id = global_data.get_new_user_id()
        else:
            self.id = id
        
        self.discord_id = discord_id
        self.discord_name = discord_name
        self.discord_discriminator = discord_discriminator

    def __eq__(self, o: object) -> bool:
        return  isinstance(o, User) and self.discord_id == o.discord_id
