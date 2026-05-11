import os
from decimal import Decimal, InvalidOperation
from typing import Any, Optional

import psycopg
from dotenv import load_dotenv

load_dotenv()

_SCHEMA_INITIALIZED = False

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS price_snapshots (
    id BIGSERIAL PRIMARY KEY,
    item_id BIGINT,
    product_id BIGINT,
    url TEXT,
    name TEXT,
    image TEXT,
    price NUMERIC(10, 2),
    discount NUMERIC(10, 2),
    limited_offer BOOLEAN,
    stock TEXT,
    source TEXT,
    scraped_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_price_snapshots_item_id ON price_snapshots (item_id);
CREATE INDEX IF NOT EXISTS idx_price_snapshots_scraped_at ON price_snapshots (scraped_at DESC);
"""


def _database_url() -> Optional[str]:
    return os.getenv("DATABASE_URL")


def get_conn():
    url = _database_url()
    if not url:
        raise RuntimeError("DATABASE_URL is not set")
    return psycopg.connect(url, autocommit=True)


def init_schema() -> None:
    global _SCHEMA_INITIALIZED
    if _SCHEMA_INITIALIZED:
        return
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(SCHEMA_SQL)
    _SCHEMA_INITIALIZED = True


def _to_decimal(value: Any) -> Optional[Decimal]:
    if value is None:
        return None
    if isinstance(value, Decimal):
        return value
    if isinstance(value, (int, float)):
        try:
            return Decimal(str(value))
        except InvalidOperation:
            return None
    s = str(value).strip().replace("$", "").replace(",", "")
    if not s:
        return None
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


def _to_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, list):
        value = value[0] if value else None
    if value is None:
        return None
    s = str(value).strip()
    if not s:
        return None
    try:
        return int(s)
    except (ValueError, TypeError):
        return None


def save_snapshot(
    *,
    item_id: Any = None,
    product_id: Any = None,
    url: Optional[str] = None,
    name: Optional[str] = None,
    image: Optional[str] = None,
    price: Any = None,
    discount: Any = None,
    limited_offer: Optional[bool] = None,
    stock: Optional[str] = None,
    source: Optional[str] = None,
) -> None:
    if not _database_url():
        print("DATABASE_URL not set; skipping snapshot save.")
        return
    try:
        init_schema()
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO price_snapshots
                    (item_id, product_id, url, name, image, price, discount,
                     limited_offer, stock, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    _to_int(item_id),
                    _to_int(product_id),
                    url,
                    name,
                    image,
                    _to_decimal(price),
                    _to_decimal(discount),
                    limited_offer,
                    stock,
                    source,
                ),
            )
    except Exception as e:
        print(f"DB save_snapshot failed: {e}")
