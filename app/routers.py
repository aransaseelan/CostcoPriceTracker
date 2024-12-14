from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from .database import get_db
from .schemas import ItemResponse, ItemBase
from . import crud

router = APIRouter()

@router.get("/items", response_model=List[ItemResponse])
def read_items(db: Session = Depends(get_db)):
    items = crud.get_items(
        db=db,
        stock=stock,
        limited_offer=limited_offer,
        min_original_price=min_original_price,
        max_original_price=max_original_price,
        min_discount_price=min_discount_price,
        max_discount_price=max_discount_price,
    )
    if not items:
        raise HTTPException(status_code=404, detail="No items found")
    return items

@router.put("/items", response_model=ItemResponse, status_code=201)
def add_item(item_data: ItemBase, db: Session = Depends(get_db)):
    new_item = crud.create_item(db, item_data)
    if not new_item:
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    return new_item



