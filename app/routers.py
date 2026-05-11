from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List

from .schemas import ItemResponse, ItemBase, ItemFilters, PriceHistoryPoint
from . import crud

router = APIRouter()

@router.get("/items", response_model=List[ItemResponse])
def read_items(filters: ItemFilters = Depends()):
    items = crud.get_items(filters)
    return items

@router.get("/items/{item_id}/history", response_model=List[PriceHistoryPoint])
def read_item_history(item_id: int, limit: int = Query(200, ge=1, le=1000)):
    return crud.get_item_history(item_id, limit)

@router.post("/items", response_model=ItemBase, status_code=201)
def add_item(item_data: ItemBase):
    new_item = crud.create_item(item_data)
    if not new_item:
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    return new_item

@router.put("/items/{item_id}", response_model=ItemBase)
def update_item(item_id: str, item_data: ItemBase):
    updated_item = crud.update_item(item_id, item_data)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item
