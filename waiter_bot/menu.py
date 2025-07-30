import os
from typing import Any, Dict, List

import aiohttp

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")


async def get_categories() -> List[Dict[str, Any]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/categories/") as resp:
            resp.raise_for_status()
            return await resp.json()


async def get_dishes(category_id: int) -> List[Dict[str, Any]]:
    async with aiohttp.ClientSession() as session:
        url = f"{API_BASE_URL}/dishes/?category={category_id}"
        async with session.get(url) as resp:
            resp.raise_for_status()
            return await resp.json()
