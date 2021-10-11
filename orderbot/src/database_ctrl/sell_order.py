from .base import Base

from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, BigInteger, DateTime, String


class SellOrder(Base):
    __tablename__ = 'sell_order'

    id = Column(BigInteger, primary_key=True)
    buy_order_id = Column(BigInteger, ForeignKey('buy_order.id'))
    user_id = Column(BigInteger, ForeignKey('user.id'))
    date_creation = Column(DateTime)
    guild_id = Column(BigInteger)
    guild_name = Column(String)
    channel_id = Column(BigInteger)
    channel_name = Column(String)

    user = relationship('User', back_populates='sell_orders')
    buy_order = relationship('BuyOrder', back_populates='sell_orders')
    items = relationship('Item', back_populates='sell_order')

    def __repr__(self) -> str:
        return f'SellOrder(id={self.id}, buy_order_id={self.buy_order_id}, user_id={self.user_id}, date_creation={self.date_creation}, guild_id={self.guild_id}, guild_name={self.guild_name}, channel_id={self.channel_id}, channel_name={self.channel_name})' 