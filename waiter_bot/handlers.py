import os
from typing import Any, Dict, List

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from waiter_bot.db import save_order
from waiter_bot.menu import get_menu

ITEMS_PER_PAGE = 5


class OrderStates(StatesGroup):
    choosing_guests = State()
    choosing_location = State()
    choosing_table = State()
    choosing_dish = State()


def table_keyboard(location: str) -> InlineKeyboardMarkup:
    numbers = list(range(1, 16)) if location == "in" else list(range(20, 40))
    buttons: List[List[InlineKeyboardButton]] = []
    row: List[InlineKeyboardButton] = []
    for num in numbers:
        row.append(InlineKeyboardButton(text=str(num), callback_data=f"table:{num}"))
        if len(row) == 5:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def guests_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=str(i), callback_data=f"guests:{i}")]
        for i in range(1, 9)
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def location_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Inside", callback_data="loc:in")],
        [InlineKeyboardButton(text="Outside", callback_data="loc:out")],
    ]
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
        nav_row.append(InlineKeyboardButton(text="\u25C0 Назад", callback_data="prev"))
    if end < len(menu):
        nav_row.append(InlineKeyboardButton(text="Далее \u25B6", callback_data="next"))
    if nav_row:
        buttons.append(nav_row)
    buttons.append([InlineKeyboardButton(text="\u2705 Завершить заказ", callback_data="finish")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def register_handlers(dp: Dispatcher) -> None:
    dp.message.register(cmd_start, commands={"start"})
    dp.callback_query.register(guests_chosen, lambda c: c.data.startswith("guests"), OrderStates.choosing_guests)
    dp.callback_query.register(location_chosen, lambda c: c.data.startswith("loc"), OrderStates.choosing_location)
    dp.callback_query.register(table_chosen, lambda c: c.data.startswith("table"), OrderStates.choosing_table)
    dp.callback_query.register(navigate_menu, lambda c: c.data in {"next", "prev"}, OrderStates.choosing_dish)
    dp.callback_query.register(dish_chosen, lambda c: c.data.startswith("dish"), OrderStates.choosing_dish)
    dp.callback_query.register(finish_order, lambda c: c.data == "finish", OrderStates.choosing_dish)


async def cmd_start(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Сколько гостей?", reply_markup=guests_keyboard())
    await state.set_state(OrderStates.choosing_guests)


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
    await state.update_data(table_number=int(table_number), items=[], page=0)
    await call.message.edit_text("Выберите блюда:", reply_markup=menu_keyboard(menu, 0))
    await state.set_state(OrderStates.choosing_dish)


async def navigate_menu(call: types.CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    menu = await get_menu()
    page = data.get("page", 0)
    if call.data == "next":
        page += 1
    else:
        page -= 1
    total_pages = (len(menu) - 1) // ITEMS_PER_PAGE
    page = max(0, min(page, total_pages))
    await state.update_data(page=page)
    await call.message.edit_reply_markup(reply_markup=menu_keyboard(menu, page))
    await call.answer()


async def dish_chosen(call: types.CallbackQuery, state: FSMContext) -> None:
    _, dish_id = call.data.split(":")
    menu = await get_menu()
    dish_map = {d["id"]: d["name"] for d in menu}
    data = await state.get_data()
    items: List[Dict[str, Any]] = data.get("items", [])
    name = dish_map.get(int(dish_id), f"#{dish_id}")
    items.append({"id": int(dish_id), "name": name})
    await state.update_data(items=items)
    await call.answer(f"Добавлено: {name}")


async def finish_order(call: types.CallbackQuery, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    items = data.get("items", [])
    if not items:
        await call.answer("Блюда не выбраны", show_alert=True)
        return

    table_number = data.get("table_number")
    guests_count = data.get("guests_count")
    location = data.get("location", "")
    await save_order(items=items, table_number=table_number, guests_count=guests_count)
    loc_label = "Inside" if location == "in" else "Outside"
    header = f"Стол {table_number} ({loc_label}, {guests_count} гостей)"
    text = header + ":\n" + "\n".join(f"- {i['name']}" for i in items)
    bar_chat = int(os.getenv("BAR_CHAT_ID", "0"))
    if bar_chat:
        await bot.send_message(bar_chat, text)

    await call.message.edit_text("Заказ сохранён", reply_markup=None)
    await state.clear()
