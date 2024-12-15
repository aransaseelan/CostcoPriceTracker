from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Items(Base):

    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    image = Column(String(255), nullable=True)
    original_price = Column(Integer, nullable=True)
    discount_price = Column(Integer, nullable=True)
    limited_offer = Column(String(12), nullable=True)
    stock = Column(String(25), nullable=True)
    created_date = Column(DateTime(timezone=True), default=func.now())
