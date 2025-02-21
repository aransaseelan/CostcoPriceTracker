from sqlalchemy.orm import Session
from typing import Optional, List

from .models import Items
from .schemas import ItemBase, ItemFilters, ItemResponse

def get_items(db: Session, filters: ItemFilters):
    query = db.query(Items)

    if filters.stock is not None:
        query = query.filter(Items.stock == filters.stock)
    
    if filters.limited_offer is not None:
        query = query.filter(Items.limited_offer == filters.limited_offer)
    
    if filters.min_original_price is not None:
        query = query.filter(Items.original_price >= filters.min_original_price)
    
    if filters.max_original_price is not None:
        query = query.filter(Items.original_price <= filters.max_original_price)
    
    if filters.min_discount_price is not None:
        query = query.filter(Items.discount_price >= filters.min_discount_price)
    
    if filters.max_discount_price is not None:
        query = query.filter(Items.discount_price <= filters.max_discount_price)

    items = query.all()
    return [ItemResponse.from_orm(item) for item in items]

def create_item(db: Session, item_data: ItemBase) -> Items:
    existing_item = db.query(Items).filter(Items.item_id == item_data.item_id).first()
    if existing_item:
        return None

    new_item = Items(
        item_id=item_data.item_id,
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
    return ItemBase.from_orm(new_item)

def update_item(db: Session, item_id: str, item_data: ItemBase) -> Optional[ItemBase]:
    existing_item = db.query(Items).filter(Items.item_id == item_id).first()
    if not existing_item:
        return None

    for key, value in item_data.dict(exclude_unset=True).items():
        setattr(existing_item, key, value)
    
    db.commit()
    db.refresh(existing_item)
    return ItemBase.from_orm(existing_item)
