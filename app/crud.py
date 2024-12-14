from sqlalchemy.orm import Session
from typing import Optional, List

from .models import Item
from .schemas import ItemCreate

def get_items(
    db: Session,
    stock: Optional[bool] = None,
    limited_offer: Optional[bool] = None,
    min_original_price: Optional[int] = None,
    max_original_price: Optional[int] = None,
    min_discount_price: Optional[int] = None,
    max_discount_price: Optional[int] = None
) -> List[Item]:
    query = db.query(Item)

    if stock is not None:
        query = query.filter(Item.stock == stock)
    if limited_offer is not None:
        query = query.filter(Item.limited_offer == limited_offer)
    if min_original_price is not None:
        query = query.filter(Item.original_price >= min_original_price)
    if max_original_price is not None:
        query = query.filter(Item.original_price <= max_original_price)
    if min_discount_price is not None:
        query = query.filter(Item.discount_price >= min_discount_price)
    if max_discount_price is not None:
        query = query.filter(Item.discount_price <= max_discount_price)

    return query.all()

def create_item(db: Session, item_data: ItemCreate) -> Item:
    # Check if item with given ID already exists
    existing_item = db.query(Item).filter(Item.id == item_data.id).first()
    if existing_item:
        return None

    new_item = Item(
        id=item_data.id,
        url=None,
        name=None,
        image=None,
        original_price=None,
        discount_price=None,
        limited_offer=None,
        stock=None,
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item
