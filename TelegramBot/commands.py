from telegram import Update, BotCommand
from telegram.ext import ContextTypes
# try both import styles so module works whether run from project root or inside TelegramBot folder
try:
    from .keyboardes import start_panel_keyboard
    from .messages import START_MSG, HELP_MSG, SUPPORT_MSG
except Exception:
    from keyboardes import start_panel_keyboard
    from messages import START_MSG, HELP_MSG, SUPPORT_MSG

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for /start and for the persistent keyboard 'start' button.
    """
    await update.message.reply_text(
        START_MSG,
        reply_markup=start_panel_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for /help and 'راهنمایی' button.
    """
    await update.message.reply_text(
        HELP_MSG,
        reply_markup=start_panel_keyboard()
    )

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for /support and 'پشتیبانی' button.
    """
    await update.message.reply_text(
        SUPPORT_MSG,
        reply_markup=start_panel_keyboard()
    )

# Export a list of BotCommand objects for set_my_commands
COMMANDS = [
    BotCommand("start", "شروع"),
    BotCommand("help",  "راهنمایی"),
    BotCommand("support", "پشتیبانی"),
    # Optional convenience commands; actual flows use reply-keyboard:
    BotCommand("add_delivery", "ساخت چاپار"),
    BotCommand("my_chapar", "چاپار شما"),
]
