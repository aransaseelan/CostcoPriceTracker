import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base
from streamlit_sqlalchemy import StreamlitAlchemyMixin

Base = declarative_base()

class CostcoDatabase(Base, StreamlitAlchemyMixin):
    __tablename__ = 'costcodatabase'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    image = Column(String(255), nullable=True)
    original_price = Column(Integer, nullable=True)
    discount_price = Column(Integer, nullable=True)
    limited_offer = Column(String(12), nullable=True)
    stock = Column(String(25), nullable=True)
    created_date = Column(DateTime(timezone=True), default=func.now())