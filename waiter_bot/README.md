## Waiter Telegram Bot

A simple Telegram bot helps waiters take orders by fetching menu data from the
local Django API. Categories and dishes are retrieved using `aiohttp` and the
completed order is stored in SQLite.

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
# Optional base URL of the Django API
export API_BASE_URL=http://localhost:8000/api
```

3. Start the bot:

```bash
python -m waiter_bot.bot
```

The bot displays menu categories from the API, lets the waiter pick dishes,
saves the order to SQLite and optionally forwards it to the configured bar chat.
On `/start` the bot first asks for a table number before showing menu categories.
