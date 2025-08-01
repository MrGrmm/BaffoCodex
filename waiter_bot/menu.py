from typing import Any, Dict, List

# Local menu data so the bot works without the Django backend

menu_items: List[Dict[str, Any]] = [
    {"id": 1, "name": "Tagliatelle al Ragù", "price": 14.0},
    {"id": 2, "name": "Grigliata di Pesce", "price": 30.0},
    {"id": 3, "name": "Pizza Margherita", "price": 8.0},
    {"id": 4, "name": "Tiramisu", "price": 9.0},
    {"id": 5, "name": "Bruschetta", "price": 5.0},
    {"id": 6, "name": "Risotto ai Funghi", "price": 12.0},
    {"id": 7, "name": "Spaghetti Carbonara", "price": 11.0},
    {"id": 8, "name": "Insalata Caprese", "price": 7.5},
    {"id": 9, "name": "Minestrone", "price": 6.0},
    {"id": 10, "name": "Panna Cotta", "price": 7.0},
    {"id": 11, "name": "Focaccia", "price": 4.0},
    {"id": 12, "name": "Lasagna", "price": 13.0},
    {"id": 13, "name": "Pizza Pepperoni", "price": 9.0},
    {"id": 14, "name": "Gelato", "price": 6.5},
    {"id": 15, "name": "Gnocchi al Pesto", "price": 10.0},
]


async def get_menu() -> List[Dict[str, Any]]:
    """Return the static list of available dishes."""
    return menu_items
