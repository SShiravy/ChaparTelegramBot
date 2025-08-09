from enum import Enum
from telegram import Update
from Models.delivery import Delivery
from custom_logger import logger
from Database import db_methods
from telegram.ext import (
    CallbackQueryHandler, CommandHandler, MessageHandler,
    ConversationHandler, ContextTypes, filters)


class AddDeliveryStates(Enum):
    """
    we will return these states in handlers 
    and use .name parameter as a key for context.user_data
    and .value param for msgs
    """
    GET_SOURCE_ID = "لطفا آیدی کانال مبدا را ارسال کنید"
    GET_DESTINATION_ID = ("لطفا آیدی کانال مقصد را وارد کنید.\n""توجه کنید که اول باید ربات در این کانال ادمین باشد.")
    GET_DELIVARY_NAME = "یک نام دلخوام برای چاپار خود انتخاب کنین"
    

async def create_new_delivery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    the_user = db_methods.fetch_user_by_id(update.effective_user.id)
    if the_user.n_delivery >=5:
        await update.message.reply_text("شما قبلا ۵ چاپار ساخته‌اید. برای افزایش تعداد،با پشتیبانی ربات ارتباط بگیرید!")
        return ConversationHandler.END
    
    await update.message.reply_text(AddDeliveryStates.GET_SOURCE_ID.value)
    return AddDeliveryStates.GET_SOURCE_ID

async def get_source_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[AddDeliveryStates.GET_SOURCE_ID.name] \
        = update.message.text.strip()
    # TODO: Check if it is a valid chat id
    await update.message.reply_text(AddDeliveryStates.GET_DESTINATION_ID.value)
    return AddDeliveryStates.GET_DESTINATION_ID

async def get_destination_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[AddDeliveryStates.GET_DESTINATION_ID.name] \
        = update.message.text.strip()
    # TODO: Check if it is a valid chat id and bot is an admin in it
    await update.message.reply_text(AddDeliveryStates.GET_DELIVARY_NAME.value)
    return AddDeliveryStates.GET_DELIVARY_NAME

async def get_delivery_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[AddDeliveryStates.GET_DELIVARY_NAME.name] = update.message.text.strip()
    # store delivery data in a the db
    user_id = update.effective_user.id

    new_delivery = Delivery(
        name = context.user_data[AddDeliveryStates.GET_DELIVARY_NAME.name],
        user_id = user_id,
        source_id = context.user_data[AddDeliveryStates.GET_SOURCE_ID.name],
        destination_id = context.user_data[AddDeliveryStates.GET_DESTINATION_ID.name]
        )
    
    if not db_methods.add_new_delivery(new_delivery):
        await update.message.reply_text("ساخت چاپار شما با شکست مواجه شد!")
        return ConversationHandler.END
    # Update User n_delivery
    selected_user = db_methods.fetch_user_by_id(user_id)
    selected_user.n_delivery += 1
    db_methods.update_user_in_db(selected_user)
    
    logger.info(f"New delivery created; {user_id=}: {new_delivery=}")

    await update.message.reply_text("چاپار شما با موفقیت فعال شد")
    return ConversationHandler.END

async def cancel_add_delivery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ساخت چاپار لغو شد!")
    logger.info(f"User {update.effective_user} canceled add delivery")
    return ConversationHandler.END


add_delivery_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(create_new_delivery,pattern)], # TODO: fix the patter param
    states={
        AddDeliveryStates.GET_SOURCE_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_source_chat)],
        AddDeliveryStates.GET_DESTINATION_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_destination_chat)],
        AddDeliveryStates.GET_DELIVARY_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_delivery_name)]
    },
    fallbacks=[CommandHandler('cancel', cancel_add_delivery)]
)
