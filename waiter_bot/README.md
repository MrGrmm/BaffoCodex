## Waiter Telegram Bot

A simple Telegram bot helps waiters take orders using a short menu defined in `menu.py`. The completed order is stored in SQLite.

### Running the bot

1. Install dependencies (from the repository root):

```bash
pip install -r requirements.txt


### Running the bot

1. Install dependencies (from the repository root):

```bash
pip install -r requirements.txt
```

2. Set environment variables:

```bash
export BOT_TOKEN=<telegram bot token>
# Optional chat id where orders are sent
export BAR_CHAT_ID=<chat id>
export BOT_TOKEN=<telegram bot token>
# Optional chat id where orders are sent
export BAR_CHAT_ID=<chat id>

```

3. Start the bot:

```bash
python -m waiter_bot.bot

```

The bot shows a fixed menu from `menu.py`, lets the waiter add dishes page by page,  
saves the order to SQLite and optionally forwards it to the configured bar chat.  
On `/start`, the bot asks for guest count, then whether guests sit inside or outside,  
and finally the table number before showing menu pages.

