from typing import Any, Dict, List

# Реальные блюда (для вывода на кнопках)
menu_items: List[Dict[str, Any]] = [
    {"id": 1, "name": "Tagliatelle al Ragù", "price": 14.0},
    {"id": 2, "name": "Grigliata di Pesce", "price": 16.0},
    {"id": 3, "name": "Pizza Margherita", "price": 8.0},
    {"id": 4, "name": "Tiramisù", "price": 6.0},
    {"id": 5, "name": "Bruschetta", "price": 5.0},
    {"id": 6, "name": "Risotto ai Funghi", "price": 12.0},
    {"id": 7, "name": "Spaghetti Carbonara", "price": 11.0},
    {"id": 8, "name": "Insalata Caprese", "price": 7.5},
    {"id": 9, "name": "Minestrone", "price": 6.0},
    {"id": 10, "name": "Bistecca Controfiletto", "price": 17.0},
    {"id": 11, "name": "Focaccia", "price": 4.0},
    {"id": 12, "name": "Lasagna", "price": 13.0},
    {"id": 13, "name": "Pizza Peperoni", "price": 9.0},
    {"id": 14, "name": "Gelato", "price": 6.5},
    {"id": 15, "name": "Gnocchi al Pesto", "price": 10.0},
]

# Категории
CATEGORIES = [
    {"id": 1, "name": "Пицца"},
    {"id": 2, "name": "Паста"},
]

# Блюда по категориям (id синтетический)
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

# Возвращает список всех блюд (не по категориям)
async def get_menu() -> List[Dict[str, Any]]:
    """Return the static list of available dishes."""
    return menu_items

# Возвращает список категорий
async def get_categories() -> List[Dict]:
    return CATEGORIES

# Возвращает список блюд по категории
async def get_dishes(category_id: int) -> List[Dict]:
    return DISHES.get(category_id, [])
