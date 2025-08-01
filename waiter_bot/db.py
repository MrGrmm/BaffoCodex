import json
import os
import aiosqlite

DB_PATH = os.path.join(os.path.dirname(__file__), "orders.db")

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_number INTEGER NOT NULL,
    guests_count INTEGER NOT NULL,
    items TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(CREATE_TABLE_SQL)
        await db.commit()

async def save_order(items: list, table_number: int, guests_count: int) -> None:
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO orders (table_number, guests_count, items) VALUES (?, ?, ?)",
            (table_number, guests_count, json.dumps(items)),
        )
        await db.commit()
