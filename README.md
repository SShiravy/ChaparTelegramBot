# ChaparTelegramBot

Chapar (چاپار) is a Telegram bot that relays new posts from a source channel to a destination channel. Each source→destination pair is called a **chapar**, or *delivery*.

Users create and manage their chapars through a Persian-language Telegram bot. A separate user-account bot (a regular Telegram account driven by Pyrogram) joins the source channels, picks up new messages, and has the bot repost them to the destination channels.

## How it works

The project runs as two processes that share one SQLite database:

| Process | Entry point | Library | Role |
|---|---|---|---|
| **Telegram Bot** | `run_chapar_telegram_bot.py` | python-telegram-bot | The interface users talk to: registers users and creates, lists, enables and disables chapars. |
| **User Bot** | `run_user_bot.py` | Pyrogram | A real Telegram account. It joins source channels, reads new messages and sends them to destinations through the Telegram Bot. |

The user-bot loop (`UserBot/user_bot_loop.py`) runs every `USER_BOT_SLEEP_TIME` seconds and works through all active deliveries:

1. **New delivery:** join the source chat, store the ID of its latest message as `last_forwarded_msg_id`, and mark the delivery as joined.
2. **Existing delivery:** read the last 100 messages in the source, collect those newer than `last_forwarded_msg_id`, and send them to the destination oldest-first. It then updates the forwarded-message counter.

Supported message types are text, photo, video, animation, document, sticker and link previews.

> The bot must be an **admin** in the destination channel to post there.

## Project structure

```
ChaparBotProject/
├── config.py                    # Settings loaded from .env (pydantic-settings)
├── custom_logger.py             # Root logger setup (console + file)
├── run_chapar_telegram_bot.py   # Starts the Telegram Bot (also creates DB tables)
├── run_user_bot.py              # Starts the User Bot polling loop
├── Database/
│   ├── database.py              # SQLite engine + create_tables()
│   └── db_methods.py            # CRUD helpers for users and deliveries
├── Models/
│   ├── user.py                  # User model (superuser / customer / friend, premium)
│   └── delivery.py              # Delivery model (source, destination, state, counters)
├── TelegramBot/
│   ├── bot.py                   # Application setup and handler registration
│   ├── commands.py              # /start, /help, /support
│   ├── add_delivery_flow.py     # Conversation: create a new chapar
│   ├── get_delivery_info_flow.py# Conversation: list / control existing chapars
│   ├── keyboardes.py            # Reply and inline keyboards
│   ├── messages.py              # User-facing (Persian) message strings
│   └── methods.py               # send_message_to_chat() used by the User Bot
└── UserBot/
    ├── account_bot.py           # DeliveryBot wrapper around a Pyrogram Client
    ├── proxy_setting.py         # Reads the Windows system proxy (optional)
    └── user_bot_loop.py         # Delivery polling/forwarding loop
```

## Requirements

- Python 3.10+
- A bot token from [@BotFather](https://t.me/BotFather)
- A Telegram account, with `api_id` and `api_hash` from [my.telegram.org](https://my.telegram.org)

Install the dependencies:

```bash
pip install python-telegram-bot==22.3 pyrogram==2.0.106 tgcrypto sqlmodel==0.0.24 pydantic-settings==2.10.1
```

`tgcrypto` is optional, but it makes Pyrogram much faster.

## Configuration

Create a `.env` file in the project root:

```env
# Database
DATABASE_NAME=ChaparBOT.db

# Telegram Bot
TELEGRAM_BOT_TOKEN=123456:ABC-your-bot-token

# User Bot
USER_BOT_API_ID=1234567
USER_BOT_API_HASH=your_api_hash
USER_BOT_STR_SESSION=your_pyrogram_session_string
USER_BOT_USE_PROXY=false
USER_BOT_SLEEP_TIME=60
```

| Variable | Description |
|---|---|
| `DATABASE_NAME` | Path to the SQLite database file. |
| `TELEGRAM_BOT_TOKEN` | Token of the bot users talk to. |
| `USER_BOT_API_ID` / `USER_BOT_API_HASH` | API credentials of the user account. |
| `USER_BOT_STR_SESSION` | Pyrogram session string of the user account (see below). |
| `USER_BOT_USE_PROXY` | If `true`, the User Bot connects through the Windows system proxy. |
| `USER_BOT_SLEEP_TIME` | Seconds to wait between polling rounds. |

### Generating a session string

Run this once and log in with your phone number when prompted. Paste the printed string into `USER_BOT_STR_SESSION`:

```python
import asyncio
from UserBot.account_bot import DeliveryBot

print(
    asyncio.run(DeliveryBot.generate_str_session(API_ID, "API_HASH", use_proxy=False))
)
```

Keep the session string secret, because it gives full access to the account.

### Proxy

`UserBot/proxy_setting.py` reads the proxy from the Windows registry (`HKCU\...\Internet Settings`), so `USER_BOT_USE_PROXY=true` only works on Windows. On other platforms, set it to `false`.

## Running

Start both processes, each in its own terminal:

```bash
python run_chapar_telegram_bot.py
python run_user_bot.py
```

Start the Telegram Bot first, because it creates the database tables on startup. Each process writes logs to the console and to a log file (`TelegramBot.log` and `AccountBot.log`).

## Using the bot

Open the bot in Telegram and send `/start`. The main keyboard offers these buttons:

- **ساخت چاپار** (create chapar): send the source channel ID, then the destination channel ID (the bot must be an admin there), then a name.
- **📋 چاپار شما** (your chapars): list your chapars. You can enable or disable each one and see a summary.
- **ℹ️ راهنمایی** (help) / **🆘 پشتیبانی** (support)

Slash commands: `/start`, `/help`, `/support`.

By default, each user can create up to 5 chapars.

## License

[MIT](LICENSE) © 2025 Soheil Shiravy
