# TelegramBot/get_delivery_info_flow.py
from enum import Enum
from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
from Database import db_methods
from .keyboardes import all_deliveries_panel, delivery_control_pannel
from typing import Optional


class DeliveryInfoStates(Enum):
    """
    Conversation states for listing/selecting deliveries and taking actions.
    """

    SELECT_DELIVERY = 1
    ACTION_CHOICE = 2


async def list_deliveries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Entry point: user clicked "📋 چاپار شما" (MessageHandler).
    Show inline list of user's deliveries or a 'no deliveries' message.
    """
    user_id = str(update.effective_user.id)
    markup = all_deliveries_panel(user_id)

    if not markup:
        await update.message.reply_text("شما هنوز چاپار خود را نساخته اید!")
        return ConversationHandler.END

    await update.message.reply_text("📋 لیست چاپار های شما:", reply_markup=markup)
    return DeliveryInfoStates.SELECT_DELIVERY


async def select_delivery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Callback when user selects a delivery button (callback_data="delivery:<id>").
    Show the delivery control panel and store selected id in user_data.
    """
    query = update.callback_query
    await query.answer()

    data = query.data  # like "delivery:42"
    #
    if not data or not data.startswith("delivery:"):
        await query.message.reply_text("خطا: شناسه چاپار نامعتبر است.")
        return ConversationHandler.END

    try:
        delivery_id = int(data.split(":", 1)[1])
    except ValueError:
        await query.message.reply_text("خطا: شناسه چاپار نامعتبر است.")
        return ConversationHandler.END

    delivery = db_methods.fetch_delivery_by_id(delivery_id)
    if delivery is None:
        await query.edit_message_text("چاپار مورد نظر وجود ندارد.")
        return ConversationHandler.END

    # store selected delivery id for next actions
    context.user_data["selected_delivery_id"] = delivery_id

    # show control panel
    text = f"شما چاپار «{delivery.name}» را انتخاب کردید."
    await query.edit_message_text(text, reply_markup=delivery_control_pannel())
    return DeliveryInfoStates.ACTION_CHOICE


async def handle_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle enable/disable/summary/back_to_menu actions from delivery_control_pannel.
    """
    query = update.callback_query
    await query.answer()
    action = query.data  # enable | disable | summary | back_to_menu

    if action == "back_to_menu":
        # Return to main menu (end conversation). The main menu is a reply keyboard shown elsewhere.
        await query.edit_message_text("بازگشت به منوی اصلی.")
        return ConversationHandler.END

    delivery_id = context.user_data.get("selected_delivery_id")
    if delivery_id is None:
        await query.edit_message_text("خطا: هیچ چاپاری انتخاب نشده است.")
        return ConversationHandler.END

    delivery = db_methods.fetch_delivery_by_id(delivery_id)
    if delivery is None:
        await query.edit_message_text("چاپار یافت نشد (ممکن است حذف شده باشد).")
        return ConversationHandler.END

    # Perform the selected action
    if action == "enable":
        delivery.active = True
        ok = db_methods.update_delivery_in_db(delivery)
        if ok:
            text = f"✅ چاپار «{delivery.name}» فعال شد."
        else:
            text = "خطا در فعال‌سازی چاپار. لطفا دوباره تلاش کنید."
        await query.edit_message_text(text, reply_markup=delivery_control_pannel())
        return DeliveryInfoStates.ACTION_CHOICE

    if action == "disable":
        delivery.active = False
        ok = db_methods.update_delivery_in_db(delivery)
        if ok:
            text = f"⛔️ چاپار «{delivery.name}» غیرفعال شد."
        else:
            text = "خطا در غیرفعال‌سازی چاپار. لطفا دوباره تلاش کنید."
        await query.edit_message_text(text, reply_markup=delivery_control_pannel())
        return DeliveryInfoStates.ACTION_CHOICE

    if action == "summary":
        text_lines = [
            f"📊 خلاصهٔ چاپار «{delivery.name}»:",
            f"• شناسه: {delivery.id}",
            f"• منبع (source): {delivery.source_id}",
            f"• مقصد (destination): {delivery.destination_id}",
            f"• تعداد پیام‌های فوروارد شده: {getattr(delivery, 'n_forwarded_msg', 0)}",
            f"• وضعیت: {'فعال' if delivery.active else 'غیرفعال'}",
        ]
        await query.edit_message_text(
            "\n".join(text_lines), reply_markup=delivery_control_pannel()
        )
        return DeliveryInfoStates.ACTION_CHOICE

    # Unknown action
    await query.edit_message_text("عملیات نامعتبر.")
    return ConversationHandler.END


# Export a ConversationHandler you can add in bot.py
get_delivery_conversation = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^📋 چاپار شما$"), list_deliveries)],
    states={
        DeliveryInfoStates.SELECT_DELIVERY: [
            CallbackQueryHandler(select_delivery, pattern=r"^delivery:\d+$")
        ],
        DeliveryInfoStates.ACTION_CHOICE: [
            CallbackQueryHandler(
                handle_action, pattern=r"^(enable|disable|summary|back_to_menu)$"
            )
        ],
    },
    fallbacks=[],
    allow_reentry=True,
)
