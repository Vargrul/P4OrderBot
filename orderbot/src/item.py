class Item:
    def __init__(self, name: str, count: int, alias=[]):
        self.count = count
        self.name = name
        self.alias = alias

    # def __str__(self) -> str:
    #     pass

    def is_item(slef, desc):
        return self.alias.find(desc) or desc == self.name

    def __str__(self) -> str:
        retStr = f'{self.name} \t {self.count}'
        return retStr