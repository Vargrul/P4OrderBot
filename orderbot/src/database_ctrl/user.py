from .base import Base

from sqlalchemy.orm import relationship
from sqlalchemy import Column, BigInteger, Integer, String

# class User:
#     def __init__(self, name: str, prioity: int, alias: str="", disc: str="", id: int=None, discord_id: int= None, discord_name: str=None, discord_discriminator: int=None) -> None:
#         self.name = name
#         self.priority = prioity
#         self.disc = disc
#         self.alias = alias
#         if id is None:
#             self.id = global_data.get_new_user_id()
#         else:
#             self.id = id
        
#         self.discord_id = discord_id
#         self.discord_name = discord_name
#         self.discord_discriminator = discord_discriminator

class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    priority = Column(Integer)
    disc = Column(String)
    alias = Column(String)
    discord_id = Column(BigInteger)
    discord_name = Column(String)
    discord_discriminator = Column(String)

    buy_orders = relationship('BuyOrder', back_populates='user')
    sell_orders = relationship('SellOrder', back_populates='user')

    def __repr__(self) -> str:
        return f'User(id={self.id}, name={self.name}, priority={self.priority}, disc={self.disc}, alias={self.alias}, discord_id={self.discord_id}, discord_name={self.discord_name}, discord_discriminator={self.discord_discriminator})'

    def __eq__(self, o: object) -> bool:
        return  self.id == o.id
