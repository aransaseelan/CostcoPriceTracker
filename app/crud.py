from datetime import datetime, timezone
from typing import List, Optional

from .schemas import ItemBase, ItemFilters, ItemResponse

# Simple in-memory store to replace the previous SQLAlchemy database
_items: List[ItemResponse] = []
_next_id: int = 1


def _matches_filters(item: ItemResponse, filters: ItemFilters) -> bool:
    if filters.item_id is not None and item.item_id != filters.item_id:
        return False
    if filters.stock is not None and item.stock != filters.stock:
        return False
    if filters.limited_offer is not None and item.limited_offer != filters.limited_offer:
        return False
    if filters.min_original_price is not None:
        if item.original_price is None or item.original_price < filters.min_original_price:
            return False
    if filters.max_original_price is not None:
        if item.original_price is None or item.original_price > filters.max_original_price:
            return False
    if filters.min_discount_price is not None:
        if item.discount_price is None or item.discount_price < filters.min_discount_price:
            return False
    if filters.max_discount_price is not None:
        if item.discount_price is None or item.discount_price > filters.max_discount_price:
            return False
    return True


def get_items(filters: ItemFilters) -> List[ItemResponse]:
    return [item for item in _items if _matches_filters(item, filters)]


def create_item(item_data: ItemBase) -> Optional[ItemBase]:
    global _next_id

    if any(item.item_id == item_data.item_id for item in _items):
        return None

    new_item = ItemResponse(
        id=_next_id,
        item_id=item_data.item_id,
        url=None,
        name=None,
        image=None,
        original_price=None,
        discount_price=None,
        limited_offer=None,
        stock=None,
        created_date=datetime.now(timezone.utc),
    )
    _next_id += 1
    _items.append(new_item)
    return ItemBase(item_id=new_item.item_id)


def update_item(item_id: str, item_data: ItemBase) -> Optional[ItemBase]:
    for item in _items:
        if str(item.item_id) == str(item_id):
            payload = item_data.dict(exclude_unset=True)
            if "item_id" in payload:
                item.item_id = payload["item_id"]
            return ItemBase(item_id=item.item_id)
    return None
