# Импорт поправлен
from waiter_bot.db import save_order
from waiter_bot.menu import get_menu, get_categories, get_dishes
from waiter_bot.handlers import register_handlers

ITEMS_PER_PAGE = 5

# ...

def location_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Inside", callback_data="loc:in")],
        [InlineKeyboardButton(text="Outside", callback_data="loc:out")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def table_keyboard(location: str = "") -> InlineKeyboardMarkup:
    numbers = list(range(1, 9)) if location == "in" else list(range(20, 40))
    buttons = []
    row = []
    for num in numbers:
        row.append(InlineKeyboardButton(text=str(num), callback_data=f"table:{num}"))
        if len(row) == 5:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def menu_keyboard(menu: List[Dict[str, Any]], page: int) -> InlineKeyboardMarkup:
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    buttons = [
        [InlineKeyboardButton(text=item["name"], callback_data=f"dish:{item['id']}")]
        for item in menu[start:end]
    ]
    nav_row = []
    if start > 0:
        nav_row.append(InlineKeyboardButton(text="⬅️ Назад", callback_data="prev"))
    if end < len(menu):
        nav_row.append(InlineKeyboardButton(text="Далее ➡️", callback_data="next"))
    if nav_row:
        buttons.append(nav_row)
    buttons.append([InlineKeyboardButton(text="✅ Завершить заказ", callback_data="finish")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def cmd_start(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Сколько гостей?", reply_markup=guests_keyboard())
    await state.set_state(OrderStates.choosing_guests)


async def guests_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=str(i), callback_data=f"guests:{i}")]
        for i in range(1, 9)
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def guests_chosen(call: types.CallbackQuery, state: FSMContext) -> None:
    _, count = call.data.split(":")
    await state.update_data(guests_count=int(count))
    await call.message.edit_text("Inside or Outside?", reply_markup=location_keyboard())
    await state.set_state(OrderStates.choosing_location)


async def location_chosen(call: types.CallbackQuery, state: FSMContext) -> None:
    _, loc = call.data.split(":")
    await state.update_data(location=loc)
    await call.message.edit_text("Выберите номер стола:", reply_markup=table_keyboard(loc))
    await state.set_state(OrderStates.choosing_table)


async def table_chosen(call: types.CallbackQuery, state: FSMContext) -> None:
    _, table_number = call.data.split(":")
    menu = await get_menu()
    await state.update_data(table_number=int(table_number), items=[], page=0, dish_map={d["id"]: d["name"] for d in menu})
    await call.message.edit_text("Выберите блюдо:", reply_markup=menu_keyboard(menu, 0))
    await state.set_state(OrderStates.choosing_dish)


async def navigate_menu(call: types.CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    menu = await get_menu()
    page = data.get("page", 0)
    if call.data == "next":
        page += 1
    else:
        page = max(0, page - 1)
    total_pages = (len(menu) - 1) // ITEMS_PER_PAGE
    page = min(page, total_pages)
    await state.update_data(page=page)
    await call.message.edit_reply_markup(reply_markup=menu_keyboard(menu, page))
    await call.answer()


async def dish_chosen(call: types.CallbackQuery, state: FSMContext) -> None:
    _, dish_id = call.data.split(":")
    data = await state.get_data()
    dish_map = data.get("dish_map", {})
    items = data.get("items", [])
    name = dish_map.get(int(dish_id), f"#{dish_id}")
    items.append({"id": int(dish_id), "name": name})
    await state.update_data(items=items)
    categories = await get_categories()
    await call.message.edit_text("Выберите категорию:", reply_markup=categories_keyboard(categories))
    await state.set_state(OrderStates.choosing_category)


def categories_keyboard(categories: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=c["name"], callback_data=f"cat:{c['id']}")]
        for c in categories
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def category_chosen(call: types.CallbackQuery, state: FSMContext) -> None:
    _, cat_id = call.data.split(":")
    dishes = await get_dishes(int(cat_id))
    await call.message.edit_text("Выберите блюдо:", reply_markup=dishes_keyboard(dishes))
    await state.set_state(OrderStates.choosing_dish)


def dishes_keyboard(dishes: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text=d["name"], callback_data=f"dish:{d['id']}")]
        for d in dishes
    ]
    kb.append([InlineKeyboardButton(text="✅ Завершить заказ", callback_data="finish")])
    return InlineKeyboardMarkup(inline_keyboard=kb)
