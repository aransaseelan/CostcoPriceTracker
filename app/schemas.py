from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    id: int

class ItemCreate(ItemBase):
    # Only requiring ID for now when creating
    # Fields that will be filled by GitHub Actions are optional or will be null
    pass

class ItemResponse(BaseModel):
    id: int
    url: Optional[str]
    name: Optional[str]
    image: Optional[str]
    original_price: Optional[int]
    discount_price: Optional[int]
    limited_offer: Optional[bool]
    stock: Optional[bool]
    created_date: datetime

    class Config:
        orm_mode = True
