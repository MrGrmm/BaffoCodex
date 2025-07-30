import json
import os
import aiosqlite

DB_PATH = os.path.join(os.path.dirname(__file__), "orders.db")

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    waiter_name TEXT,
    table_number INTEGER,
    items TEXT NOT NULL
)
"""

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(CREATE_TABLE_SQL)
        await db.commit()

async def save_order(items: list, waiter_name: str | None = None, table_number: int | None = None) -> None:
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO orders (waiter_name, table_number, items) VALUES (?, ?, ?)",
            (waiter_name, table_number, json.dumps(items)),
        )
        await db.commit()
