from typing import List, Dict

CATEGORIES = [
    {"id": 1, "name": "Пицца"},
    {"id": 2, "name": "Паста"},
]

DISHES = {
    1: [  # Пицца
        {"id": 101, "name": "Маргарита"},
        {"id": 102, "name": "Пепперони"},
    ],
    2: [  # Паста
        {"id": 201, "name": "Карбонара"},
        {"id": 202, "name": "Болоньезе"},
    ]
}


async def get_categories() -> List[Dict]:
    return CATEGORIES


async def get_dishes(category_id: int) -> List[Dict]:
    return DISHES.get(category_id, [])
