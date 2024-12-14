from sqlalchemy.orm import Session
from typing import Optional, List

from .models import Items
from .schemas import ItemBase, ItemFilters

def get_items( db: Session, filters: ItemFilters) -> List[Items]:
    query = db.query(Items)

    if stock is not None:
        query = query.filter(Items.stock == stock)
    if limited_offer is not None:
        query = query.filter(Items.limited_offer == limited_offer)
    if min_original_price is not None:
        query = query.filter(Items.original_price >= min_original_price)
    if max_original_price is not None:
        query = query.filter(Items.original_price <= max_original_price)
    if min_discount_price is not None:
        query = query.filter(Items.discount_price >= min_discount_price)
    if max_discount_price is not None:
        query = query.filter(Items.discount_price <= max_discount_price)

    return query.all()

def create_item(db: Session, item_data: ItemBase) -> Items:
    # Check if item with given ID already exists
    existing_item = db.query(Items).filter(Items.id == item_data.id).first()
    if existing_item:
        return None

    new_item = Items(
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
