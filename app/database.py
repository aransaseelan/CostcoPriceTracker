import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base
from streamlit_sqlalchemy import StreamlitAlchemyMixin

Base = declarative_base()


class CostcoDatabase(Base, StreamlitAlchemyMixin):
    __tablename__ = 'costcodatabase'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    image = Column(String(255), nullable=False)
    original_price = Column(Integer, nullable=False)
    discount_price = Column(Integer, nullable=False)
    limited_offer = Column(String(12), nullable=False)
    stock = Column(String(25), nullable=False)
    created_date = Column(DateTime(timezone=True), default=func.now())

DATABASE_URL = 'sqlite:///costco_database.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def create_connection():
    Base.metadata.create_all(engine)

def insert_data(url, name, price, image, discount, limited_offer, stock):
    new_entry = CostcoDatabase(
        url=url,
        name=name,
        original_price=price,
        image=image,
        discount_price=discount,
        limited_offer=limited_offer,
        stock=stock
    )
    session.add(new_entry)
    session.commit()

def check_database():
    results = session.query(CostcoDatabase).all()
    for result in results:
        st.write(result.name, result.original_price, result.discount_price, result.stock)

def reset_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    print('Database created successfully')
    create_connection()
    st.title('Costco Database Viewer')
    
    if st.button('Reset Database'):
        reset_database()
        st.success('Database reset successfully')
    
    if st.button('Insert Sample Data'):
        insert_data('http://example.com', 'Sample Product', 100, 'image_url', 80, 'Limited Offer', 'In Stock')
        st.success('Sample data inserted successfully')
    
    st.write('Current Database Entries:')
    check_database()
