import os
from typing import Any, Dict, List

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .db import save_order
from .menu import get_categories, get_dishes


class OrderStates(StatesGroup):
    choosing_table = State()
    choosing_category = State()
    choosing_dish = State()


def categories_keyboard(categories: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=c["name"], callback_data=f"cat:{c['id']}")]
        for c in categories
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def table_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=str(i), callback_data=f"table:{i}")]
        for i in range(1, 9)
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def dishes_keyboard(dishes: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text=d["name"], callback_data=f"dish:{d['id']}")]
        for d in dishes
    ]
    kb.append([InlineKeyboardButton(text="\u2705 Завершить заказ", callback_data="finish")])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def register_handlers(dp: Dispatcher) -> None:
    dp.message.register(cmd_start, commands={"start"})
    dp.callback_query.register(table_chosen, lambda c: c.data.startswith("table"), OrderStates.choosing_table)
    dp.callback_query.register(category_chosen, lambda c: c.data.startswith("cat"), OrderStates.choosing_category)
    dp.callback_query.register(dish_chosen, lambda c: c.data.startswith("dish"), OrderStates.choosing_dish)
    dp.callback_query.register(finish_order, lambda c: c.data == "finish", OrderStates.choosing_dish)


async def cmd_start(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Выберите номер стола:", reply_markup=table_keyboard())
    await state.set_state(OrderStates.choosing_table)


async def table_chosen(call: types.CallbackQuery, state: FSMContext) -> None:
    _, table_number = call.data.split(":")
    await state.update_data(table_number=int(table_number))
    categories = await get_categories()
    await call.message.edit_text(
        "Выберите категорию:", reply_markup=categories_keyboard(categories)
    )
    await state.set_state(OrderStates.choosing_category)


async def category_chosen(call: types.CallbackQuery, state: FSMContext) -> None:
    _, cat_id = call.data.split(":")
    dishes = await get_dishes(int(cat_id))
    dish_map = {d["id"]: d["name"] for d in dishes}
    await state.update_data(items=[], dish_map=dish_map)
    await call.message.edit_text("Выберите блюда:", reply_markup=dishes_keyboard(dishes))
    await state.set_state(OrderStates.choosing_dish)


async def dish_chosen(call: types.CallbackQuery, state: FSMContext) -> None:
    _, dish_id = call.data.split(":")
    data = await state.get_data()
    dish_map: Dict[int, str] = data.get("dish_map", {})
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
    await save_order(items=items, table_number=table_number)
    header = f"Стол {table_number}" if table_number else "Новый заказ"
    text = header + ":\n" + "\n".join(f"- {i['name']}" for i in items)
    bar_chat = int(os.getenv("BAR_CHAT_ID", "0"))
    if bar_chat:
        await bot.send_message(bar_chat, text)

    await call.message.edit_text("Заказ сохранён", reply_markup=None)
    await state.clear()
