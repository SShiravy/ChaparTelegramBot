from telegram import Update, BotCommand
from telegram.ext import ContextTypes
from TelegramBot.keyboardes import start_panel_keyboard
from TelegramBot.messages import START_MSG, HELP_MSG, SUPPORT_MSG, CRASH_MSG
from Database.db_methods import add_new_user
from Models.user import User, UserType


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for /start and for the persistent keyboard 'start' button.
    """

    res = add_new_user(
        User(
            account_id=str(update.effective_user.id),
            username=update.effective_user.username,
            user_type=UserType.CUSTOMER,
        )
    )
    if res is False:
        await update.message.reply_text(CRASH_MSG, reply_markup=start_panel_keyboard())
    await update.message.reply_text(START_MSG, reply_markup=start_panel_keyboard())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for /help and 'راهنمایی' button.
    """
    await update.message.reply_text(HELP_MSG, reply_markup=start_panel_keyboard())


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for /support and 'پشتیبانی' button.
    """
    await update.message.reply_text(SUPPORT_MSG, reply_markup=start_panel_keyboard())


# Export a list of BotCommand objects for set_my_commands
COMMANDS = [
    BotCommand("start", "شروع"),
    BotCommand("help", "راهنمایی"),
    BotCommand("support", "پشتیبانی"),
    # Optional convenience commands; actual flows use reply-keyboard:
    BotCommand("add_delivery", "ساخت چاپار"),
    BotCommand("my_chapar", "چاپار شما"),
]
