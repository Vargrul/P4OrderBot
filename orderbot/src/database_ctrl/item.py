from .base import Base
from orderbot.src.global_data import P4ItemEnum, P4_ITEM_ALIAS

from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, BigInteger, Enum, Integer

class Item(Base):
    __tablename__ = 'item'

    id = Column(BigInteger, primary_key=True)
    type = Column(Enum(P4ItemEnum))
    quantity = Column(Integer)
    buy_order_id = Column(BigInteger, ForeignKey('buy_order.id'))
    sell_order_id = Column(BigInteger, ForeignKey('sell_order.id'))

    buy_order = relationship('BuyOrder', back_populates='items')
    sell_order = relationship('SellOrder', back_populates='items')

    @classmethod
    def from_string_and_count(cls, item_str: str, count: int):
        item = cls()
        # Set Type
        for key in P4_ITEM_ALIAS:
            if item_str in P4_ITEM_ALIAS[key]:
                item.type = key

        # Set quantity
        item.quantity = count

        return item
    
    def __repr__(self) -> str:
        return f'Item(id={self.id}, type={self.type}, quantity={self.quantity}, buy_order_id={self.buy_order_id}, sell_order_id={self.sell_order_id})'

    def __str__(self) -> str:
        retStr = f'{self.name} \t {self.count}'
        return retStr

    def __eq__(self, o: object) -> bool:
        return o.type == self.type
