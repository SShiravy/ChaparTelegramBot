from enum import Enum
from telegram import Update
from telegram.error import BadRequest
from Models.delivery import Delivery
from Models.user import User, UserType
from Database import db_methods
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
from TelegramBot.messages import CRASH_MSG
import logging


class AddDeliveryStates(Enum):
    """
    we will return these states in handlers
    and use .name parameter as a key for context.user_data
    and .value param for msgs
    """

    GET_SOURCE_ID = "لطفا آیدی کانال مبدا را ارسال کنید"
    GET_DESTINATION_ID = (
        "لطفا آیدی کانال مقصد را وارد کنید.\n"
        "توجه کنید که اول باید ربات در این کانال ادمین باشد."
    )
    GET_DELIVARY_NAME = "یک نام دلخواه برای چاپار خود انتخاب کنید"


async def create_new_delivery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Entry point for creating a delivery.
    Ensure the user exists in DB and hasn't exceeded quota.
    """
    user_account_id = str(update.effective_user.id)
    the_user = db_methods.fetch_user_by_id(user_account_id)

    if the_user is None:
        res = db_methods.add_new_user(
            User(
                account_id=str(update.effective_user.id),
                username=update.effective_user.username,
                user_type=UserType.CUSTOMER,
            )
        )
        if res is False:
            await update.message.reply_text(
                CRASH_MSG, reply_markup=start_panel_keyboard()
            )
            return ConversationHandler.END

    if getattr(the_user, "n_delivery", 0) >= 5:
        await update.message.reply_text(
            "شما قبلا ۵ چاپار ساخته‌اید. برای افزایش تعداد، با پشتیبانی ربات ارتباط بگیرید!"
        )
        return ConversationHandler.END

    await update.message.reply_text(AddDeliveryStates.GET_SOURCE_ID.value)
    return AddDeliveryStates.GET_SOURCE_ID


async def get_source_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Receive source id text from user.
    Validate that get_chat(...) succeeds. If invalid -> show error and end.
    """
    user_input = update.message.text.strip()
    context.user_data[AddDeliveryStates.GET_SOURCE_ID.name] = user_input

    # Validate source chat exists
    try:
        await update.message.reply_text("در حال بررسی کانال مبدا...")
        chat = await context.bot.get_chat(user_input)
    except BadRequest as e:
        logging.info(
            f"Invalid source chat provided by {update.effective_user.id}: {user_input} - {e}"
        )
        await update.message.reply_text(
            "آیدی کانال مبدا معتبر نیست. لطفا دوباره تلاش کنید."
        )
        return ConversationHandler.END

    await update.message.reply_text(AddDeliveryStates.GET_DESTINATION_ID.value)
    return AddDeliveryStates.GET_DESTINATION_ID


async def get_destination_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Receive destination id text from user.
    Validate that destination chat exists and that the bot is admin in it.
    If not exists -> error_add_dest. If exists but bot not admin -> error_user_sub.
    """
    user_input = update.message.text.strip()
    context.user_data[AddDeliveryStates.GET_DESTINATION_ID.name] = user_input

    # 1) validate chat exists
    await update.message.reply_text("در حال بررسی کانال مقصد...")
    try:
        chat = await context.bot.get_chat(user_input)
    except BadRequest as e:
        logging.info(
            f"Invalid destination chat provided by {update.effective_user.id}: {user_input} - {e}"
        )
        await update.message.reply_text(
            "آیدی کانال مقصد معتبر نیست. لطفا دوباره تلاش کنید."
        )
        return ConversationHandler.END

    # 2) check bot membership/admin in the destination channel
    is_admin = False
    try:
        bot_member = await context.bot.get_chat_member(chat.id, context.bot.id)
        if bot_member.status in ("administrator", "creator"):
            is_admin = True
    except BadRequest as e:
        # When the member list is inaccessible or bot is not present, get_chat_member may raise BadRequest
        logging.info(f"Could not get bot membership for chat {chat.id}: {e}")
        is_admin = False
    except Exception as e:
        logging.error(
            f"Unexpected error while checking membership for chat {chat.id}: {e}"
        )
        is_admin = False

    if not is_admin:
        await update.message.reply_text(
            "ربات در کانال مقصد ادمین نیست. لطفا ابتدا ربات را به عنوان ادمین اضافه کنید و دوباره تلاش کنید."
        )
        return ConversationHandler.END

    # If destination is OK and bot is admin, proceed to ask for a delivery name
    await update.message.reply_text(AddDeliveryStates.GET_DELIVARY_NAME.value)
    return AddDeliveryStates.GET_DELIVARY_NAME


async def get_delivery_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Create and persist the delivery after all checks passed.
    """
    name = update.message.text.strip()
    context.user_data[AddDeliveryStates.GET_DELIVARY_NAME.name] = name

    user_account_id = str(update.effective_user.id)
    # Build a Delivery model instance
    new_delivery = Delivery(
        name=name,
        user_account_id=str(update.effective_user.id),
        source_id=context.user_data[
            AddDeliveryStates.GET_SOURCE_ID.name
        ],  # this is source username actually
        destination_id=context.user_data[AddDeliveryStates.GET_DESTINATION_ID.name],
    )

    if not db_methods.add_new_delivery(new_delivery):
        await update.message.reply_text("ساخت چاپار شما با شکست مواجه شد!")
        return ConversationHandler.END

    # update user's delivery count
    selected_user = db_methods.fetch_user_by_id(user_account_id)
    if selected_user is not None:
        selected_user.n_delivery = getattr(selected_user, "n_delivery", 0) + 1
        db_methods.update_user_in_db(selected_user)

    logging.info(
        f"New delivery created; user={user_account_id}, delivery={new_delivery}"
    )
    await update.message.reply_text("چاپار شما با موفقیت فعال شد")
    return ConversationHandler.END


async def cancel_add_delivery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ساخت چاپار لغو شد!")
    logging.info(f"User {update.effective_user.id} canceled add delivery")
    return ConversationHandler.END


add_delivery_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^ساخت چاپار$"), create_new_delivery)],
    states={
        AddDeliveryStates.GET_SOURCE_ID: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_source_chat)
        ],
        AddDeliveryStates.GET_DESTINATION_ID: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_destination_chat)
        ],
        AddDeliveryStates.GET_DELIVARY_NAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_delivery_name)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel_add_delivery)],
)
