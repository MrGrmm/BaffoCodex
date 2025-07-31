import asyncio
import os
import sys
from pathlib import Path

# Устанавливаем путь, если бот запускается напрямую
if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    __package__ = "waiter_bot"

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from waiter_bot.handlers import register_handlers

from waiter_bot.handlers import register_handlers  # <= правильный импорт

def main() -> None:
    token = '8213976596:AAFXaUgosZy36ZJLER1kP-1S8Pi_evcWcXA'  # os.getenv("BOT_TOKEN")
    if not token:
        print("BOT_TOKEN environment variable is required")
        return

    bot = Bot(token)
    dp = Dispatcher(storage=MemoryStorage())

    register_handlers(dp)

    asyncio.run(_run(bot, dp))

async def _run(bot: Bot, dp: Dispatcher) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    main()
