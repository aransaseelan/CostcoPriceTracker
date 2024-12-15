from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from .database import get_session_local 
from .schemas import ItemResponse, ItemBase, ItemFilters
import crud

router = APIRouter()

@router.get("/items", response_model=ItemResponse)
def read_items(filters: ItemFilters = Depends(),
    db: Session = Depends(get_session_local)):
    items = crud.get_items(
        db=db,
        stock=filters.stock,
        limited_offer=filters.limited_offer,
        min_original_price=filters.min_original_price,
        max_original_price=filters.max_original_price,
        min_discount_price=filters.min_discount_price,
        max_discount_price=filters.max_discount_price,
    )
    if not items:
        raise HTTPException(status_code=404, detail="No items found")
    return items

@router.post("/items", response_model=ItemResponse, status_code=201)
def add_item(item_data: ItemBase, db: Session = Depends(get_session_local)):
    new_item = crud.create_item(db, item_data)
    if not new_item:
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    return new_item



