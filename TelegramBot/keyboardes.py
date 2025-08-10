from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


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

def all_deliveries_pannel(user):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"چاپار {n}",          callback_data="")] for n in user_chapars # TODO: get user deliveires from Database
    ])

def delivery_control_pannel():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("فعال سازی",          callback_data="enable")],
        [InlineKeyboardButton("غیر فعال سازی",          callback_data="disable")],
        [InlineKeyboardButton("خلاصه",          callback_data="summary")],
    ])


