from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from Database import db_methods
from custom_logger import logger

def start_panel_keyboard():
    layout = [
        ["ساخت چاپار"],
        ["📋 چاپار شما"],
        ["ℹ️ راهنمایی","🆘 پشتیبانی"],
    ]
    return ReplyKeyboardMarkup(layout, resize_keyboard=True)


# Inline buttons
def source_decision_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ قبول",            callback_data="confirm_source")],
        [InlineKeyboardButton("🔄 دوباره وارد کنید", callback_data="retry_source")],
        [InlineKeyboardButton("↩️ بازگشت",           callback_data="back_to_menu")],
    ])

def dest_decision_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ قبول",            callback_data="confirm_dest")],
        [InlineKeyboardButton("🔄 دوباره وارد کنید", callback_data="retry_dest")],
        [InlineKeyboardButton("↩️ بازگشت",           callback_data="back_to_menu")],
    ])


def all_deliveries_panel(user_id: str) -> InlineKeyboardMarkup | None:
    """
    Build an InlineKeyboardMarkup of all deliveries for `user_id`.
    Callback data for each button will be: "delivery:<delivery_id>"

    Returns None if the user has no deliveries.
    """
    try:
        deliveries = db_methods.get_user_deliveries(user_id)
    except Exception as e:
        logger.error(f"Failed to fetch deliveries for {user_id}: {e}")
        deliveries = []

    if not deliveries:
        return None

    buttons = []
    for delivery in deliveries:
        label = delivery.name or f"چاپار {delivery.id}"
        cb = f"delivery:{delivery.id}"
        buttons.append([InlineKeyboardButton(label, callback_data=cb)])

    return InlineKeyboardMarkup(buttons)


def delivery_control_pannel():
    """
    Control panel for a single delivery — includes enable/disable/summary and a back-to-menu button.
    """
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("فعال سازی",   callback_data="enable"),
         InlineKeyboardButton("غیر فعال سازی", callback_data="disable")],
        [InlineKeyboardButton("خلاصه",       callback_data="summary")],
        [InlineKeyboardButton("↩️ بازگشت",    callback_data="back_to_menu")],
    ])
