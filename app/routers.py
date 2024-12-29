from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from .database import get_db 
from .schemas import ItemResponse, ItemBase, ItemFilters
from . import crud
from .models import Items 

router = APIRouter()

@router.get("/items", response_model=List[ItemResponse])  
def read_items(db: Session = Depends(get_db), filters: ItemFilters = Depends()):
    items = crud.get_items(db, filters)
    return items  

@router.post("/items", response_model=ItemBase, status_code=201)
def add_item(item_data: ItemBase, db: Session = Depends(get_db)):
    new_item = crud.create_item(db, item_data)
    if not new_item:
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    return new_item

