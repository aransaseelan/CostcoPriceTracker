
CREATE TABLE costcodatabase (
    item_id INTEGER PRIMARY KEY NOT NULL,
    original_price INTEGER NOT NULL,
    discount_price INTEGER NOT NULL,
    stock VARCHAR(25) NOT NULL,
    date VARCHAR(12)
);