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

def main() -> None:
    token = os.getenv("BOT_TOKEN") or '8213976596:AAF...evcWcXA'  # fallback на хардкод

    if not token:
        print("BOT_TOKEN environment variable is required")
        return

    bot = Bot(token)
    dp = Dispatcher(storage=MemoryStorage())
    register_handlers(dp)
    asyncio.run(_run(bot, dp))

    register_handlers(dp)

    asyncio.run(_run(bot, dp))

async def _run(bot: Bot, dp: Dispatcher) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    main()

