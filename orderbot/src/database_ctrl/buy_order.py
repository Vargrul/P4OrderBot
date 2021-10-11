from .base import Base
from orderbot.src.global_data import StatusEnum, P4_ITEM_ALIAS

from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, BigInteger, DateTime, Enum, String


class BuyOrder(Base):
    __tablename__ = 'buy_order'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('user.id'))
    status = Column(Enum(StatusEnum))
    date_creation = Column(DateTime)
    date_closed = Column(DateTime)
    guild_id = Column(BigInteger)
    guild_name = Column(String)
    channel_id = Column(BigInteger)
    channel_name = Column(String)

    user = relationship('User', back_populates='buy_orders')
    sell_orders = relationship('SellOrder', back_populates='buy_order')
    items = relationship('Item', back_populates='buy_order')

    def to_discord_string(self) -> str:
        response = (
            f'Issuer: **{self.user.name}** Alias: **{self.user.alias}**\n'
            f'Order ID: **{self.id}**\n```css\n'
            )
        for item in self.items:
            response = response + (f'{item.quantity:7} - {P4_ITEM_ALIAS[item.type][0]:25}\n')
        response = response + f'```'
        return response

    def __repr__(self) -> str:
        return f'BuyOrder(id={self.id}, user_id={self.user_id}, status={self.status}, date_creation={self.date_creation}, date_closed={self.date_closed}, guild_id={self.guild_id}, guild_name={self.guild_name}, channel_id={self.channel_id}, channel_name={self.channel_name})'
