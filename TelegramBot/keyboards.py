# keyboards.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

def persistent_menu_keyboard():
    layout = [
        ["➕ اضافه کردن مبدا", "➕ اضافه کردن مقصد"],
        ["ℹ️ راهنمایی",       "🆘 پشتیبانی"],
        ["📋 چاپار شما"],
    ]
    return ReplyKeyboardMarkup(layout, resize_keyboard=True)

def source_decision_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ قبول",          callback_data="confirm_source")],
        [InlineKeyboardButton("🔄 دوباره وارد کنید", callback_data="retry_source")],
        [InlineKeyboardButton("↩️ بازگشت",         callback_data="back_to_menu")],
    ])

def dest_decision_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ قبول",          callback_data="confirm_dest")],
        [InlineKeyboardButton("🔄 دوباره وارد کنید", callback_data="retry_dest")],
        [InlineKeyboardButton("↩️ بازگشت",         callback_data="back_to_menu")],
    ])
