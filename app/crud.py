from datetime import datetime, timezone










from typing import Any, List, Optional

from . import db
from .schemas import ItemBase, ItemFilters, ItemResponse, PriceHistoryPoint


def _row_to_response(row) -> ItemResponse:
    (id_, item_id, url, name, image, price, discount,
     limited_offer, stock, scraped_at) = row
    original_price = None
    discount_price = None
    if price is not None:
        discount_price = int(price)
        original_price = int(price + (discount or 0))
    stock_bool: Optional[bool] = None
    if stock is not None:
        stock_bool = stock.strip().lower() == 'in stock'
    return ItemResponse(
        id=id_,
        item_id=int(item_id) if item_id is not None else None,
        url=url,
        name=name,
        image=image,
        original_price=original_price,
        discount_price=discount_price,
        limited_offer=limited_offer,
        stock=stock_bool,
        created_date=scraped_at or datetime.now(timezone.utc),
    )


def get_items(filters: ItemFilters) -> List[ItemResponse]:
    sql = """
        SELECT DISTINCT ON (item_id)
            id, item_id, url, name, image, price, discount,
            limited_offer, stock, scraped_at
        FROM price_snapshots
        WHERE item_id IS NOT NULL
    """
    params: List[Any] = []

    if filters.item_id is not None:
        sql += " AND item_id = %s"
        params.append(filters.item_id)
    if filters.limited_offer is not None:
        sql += " AND limited_offer = %s"
        params.append(filters.limited_offer)

    sql += " ORDER BY item_id, scraped_at DESC"

    try:
        with db.get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
    except Exception as e:
        print(f"DB get_items failed: {e}")
        return []

    items = [_row_to_response(r) for r in rows]

    out: List[ItemResponse] = []
    for item in items:
        if filters.stock is not None and item.stock != filters.stock:
            continue
        if filters.min_original_price is not None and (
            item.original_price is None or item.original_price < filters.min_original_price
        ):
            continue
        if filters.max_original_price is not None and (
            item.original_price is None or item.original_price > filters.max_original_price
        ):
            continue
        if filters.min_discount_price is not None and (
            item.discount_price is None or item.discount_price < filters.min_discount_price
        ):
            continue
        if filters.max_discount_price is not None and (
            item.discount_price is None or item.discount_price > filters.max_discount_price
        ):
            continue
        out.append(item)
    return out


def get_item_history(item_id: int, limit: int = 200) -> List[PriceHistoryPoint]:
    sql = """
        SELECT scraped_at, price, discount, stock
        FROM price_snapshots
        WHERE item_id = %s
        ORDER BY scraped_at ASC
        LIMIT %s
    """
    try:
        with db.get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (item_id, limit))
            rows = cur.fetchall()
    except Exception as e:
        print(f"DB get_item_history failed: {e}")
        return []

    out: List[PriceHistoryPoint] = []
    for scraped_at, price, discount, stock in rows:
        stock_bool: Optional[bool] = None
        if stock is not None:
            stock_bool = stock.strip().lower() == 'in stock'
        out.append(PriceHistoryPoint(
            scraped_at=scraped_at or datetime.now(timezone.utc),
            price=float(price) if price is not None else None,
            discount=float(discount) if discount is not None else None,
            stock=stock_bool,
        ))
    return out


def create_item(item_data: ItemBase) -> Optional[ItemBase]:
    # Snapshots are written by the scrapers; this endpoint is a no-op stub.
    return item_data


def update_item(item_id: str, item_data: ItemBase) -> Optional[ItemBase]:
    return item_data
