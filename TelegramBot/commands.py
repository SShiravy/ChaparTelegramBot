# commands.py
from telegram import Update, BotCommand
from telegram.ext import ContextTypes
from keyboards import persistent_menu_keyboard
from messages import start_msg, help_msg, support_msg

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        start_msg,
        reply_markup=persistent_menu_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        help_msg,
        reply_markup=persistent_menu_keyboard()
    )

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        support_msg,
        reply_markup=persistent_menu_keyboard()
    )

COMMANDS = [
    BotCommand("start",           "شروع"),
    BotCommand("help",            "راهنمایی"),
    BotCommand("add_source",      "اضافه کردن مبدا"),
    BotCommand("add_destination", "اضافه کردن مقصد"),
    BotCommand("support",         "پشتیبانی"),
    BotCommand("my_chapar",       "چاپار شما"),
]
