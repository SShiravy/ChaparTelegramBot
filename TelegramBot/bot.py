import logging
import os
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

from TelegramBot.add_delivery_flow import add_delivery_handler
from TelegramBot.get_delivery_info_flow import get_delivery_conversation
from TelegramBot.messages import CRASH_MSG
from TelegramBot.commands import start, help_command, support, COMMANDS as SLASH_COMMANDS

from config import settings





# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Simple error handler
async def error_handler(update, context):
    logger.exception("Uncaught error while processing an update", exc_info=context.error)
    # Optionally notify admin, or reply to user:
    try:
        if update and update.effective_message:
            await update.effective_message.reply_text(CRASH_MSG)
    except Exception:
        # swallow to avoid recursive errors
        pass

async def _set_commands(app):
    """
    Post-init hook to set bot commands and perform DB initialization.
    """
    # set slash-commands in the Telegram UI
    try:
        await app.bot.set_my_commands(SLASH_COMMANDS)
    except Exception as e:
        logger.warning("Failed to set bot commands: %s", e)


def run_telegram_bot():
    app = (
        ApplicationBuilder()
        .token(settings.TELEGRAM_BOT_TOKEN)
        .build()
    )

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("support", support))

    # Register conversation handlers (these were created in their modules)
    # add_delivery_handler from add_delivery_flow.py
    app.add_handler(add_delivery_handler)
    # get_delivery_conversation should be defined in get_delivery_info_flow.py
    app.add_handler(get_delivery_conversation)

    # Reply-keyboard button handlers (the persistent keyboard)
    # "ساخت چاپار" is handled by the add_delivery_handler's entry point (MessageHandler)
    # "📋 چاپار شما" is handled by get_delivery_conversation's entry point
    # But we still add explicit MessageHandlers for the help/support buttons to reuse the same handlers:
    app.add_handler(MessageHandler(filters.Regex(r"^ℹ️ راهنمایی$"), help_command))
    app.add_handler(MessageHandler(filters.Regex(r"^🆘 پشتیبانی$"), support))

    # Optionally expose a handler for "ساخت چاپار" in case user presses the reply key
    app.add_handler(MessageHandler(filters.Regex(r"^ساخت چاپار$"), add_delivery_handler.entry_points[0].callback))

    # Add application-level error handler
    app.add_error_handler(error_handler)

    logger.info("Bot starting polling...")
    app.run_polling(drop_pending_updates=True)
