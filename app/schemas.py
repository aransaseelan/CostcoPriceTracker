from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    id: int
    

class ItemFilters(ItemBase):
    stock: Optional[bool] = None
    limited_offer: Optional[bool] = None
    min_original_price: Optional[int] = None
    max_original_price: Optional[int] = None
    min_discount_price: Optional[int] = None
    max_discount_price: Optional[int] = None

class ItemResponse(BaseModel):
    id: int = None
    url: Optional[str] = None
    name: Optional[str] = None
    image: Optional[str] = None
    original_price: Optional[int] = None
    discount_price: Optional[int] = None
    limited_offer: Optional[bool] = None
    stock: Optional[bool] = None
    created_date: datetime

