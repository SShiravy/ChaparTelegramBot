# main.py
import json
import logging
import asyncio
from pathlib import Path
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
)
from authentication import botToken
from commands import (
    start, help_command, support, COMMANDS as SLASH_COMMANDS
)
from handlers import (
    start_add_source, receive_source, source_decision_handler,
    start_add_dest,    receive_dest,
    show_chapar,
    STATE_SOURCE_WAIT, STATE_SOURCE_CONFIRM,
    STATE_DEST_WAIT,
)
from keyboards import persistent_menu_keyboard

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

DATA_FILE = Path("user_data.json")

async def _set_commands(app):
    # 1) register slash commands
    await app.bot.set_my_commands(SLASH_COMMANDS)

    # 2) load existing user_records if file exists
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding='utf-8'))
            app.bot_data['user_records'] = data
            logging.info(f"Loaded {len(data)} user_records from {DATA_FILE}")
        except Exception as e:
            logging.error(f"Failed to load {DATA_FILE}: {e}")
            app.bot_data['user_records'] = {}
    else:
        app.bot_data['user_records'] = {}

    # 3) ensure we also have the keyboard in bot_data
    app.bot_data['persistent_keyboard'] = persistent_menu_keyboard()

    # 4) schedule background save loop
    async def save_loop():
        while True:
            await asyncio.sleep(10)
            try:
                to_save = app.bot_data.get('user_records', {})
                DATA_FILE.write_text(
                    json.dumps(to_save, ensure_ascii=False, indent=2),
                    encoding='utf-8'
                )
                logging.debug(f"Saved {len(to_save)} user_records to {DATA_FILE}")
            except Exception as e:
                logging.error(f"Error saving {DATA_FILE}: {e}")

    asyncio.create_task(save_loop())

def main():
    app = (
        ApplicationBuilder()
        .token(botToken)
        .post_init(_set_commands)
        .build()
    )

    # Slash commands
    app.add_handler(CommandHandler("start",     start))
    app.add_handler(CommandHandler("help",      help_command))
    app.add_handler(CommandHandler("support",   support))
    app.add_handler(CommandHandler("my_chapar", show_chapar))

    # Add‑source conversation
    conv_source = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^➕ اضافه کردن مبدا$"), start_add_source)],
        states={
            STATE_SOURCE_WAIT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_source)
            ],
            STATE_SOURCE_CONFIRM: [
                CallbackQueryHandler(
                    source_decision_handler,
                    pattern="^(confirm_source|retry_source|back_to_menu)$"
                )
            ],
        },
        fallbacks=[CommandHandler("start", start)],
        allow_reentry=True,
    )
    app.add_handler(conv_source)

    # Add‑dest conversation
    conv_dest = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^➕ اضافه کردن مقصد$"), start_add_dest)],
        states={
            STATE_DEST_WAIT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_dest)
            ],
        },
        fallbacks=[CommandHandler("start", start)],
        allow_reentry=True,
    )
    app.add_handler(conv_dest)

    # Persistent‑keyboard button handlers
    app.add_handler(MessageHandler(filters.Regex(r"^ℹ️ راهنمایی$"),   help_command))
    app.add_handler(MessageHandler(filters.Regex(r"^🆘 پشتیبانی$"),     support))
    app.add_handler(MessageHandler(filters.Regex(r"^📋 چاپار شما$"),   show_chapar))

    # Start polling
    app.run_polling(drop_pending_updates=True, poll_interval=1.0)

if __name__ == "__main__":
    main()
