# handlers.py
import json
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram.error import BadRequest
from messages import (
    start_msg,
    add_source_msg,
    add_destination_msg,
    check_source,
    check_dest_sub,
    success_msg,
    add_source_done,
    add_dest_done,
    error_add_source,
    error_add_dest,
    error_user_sub,
)
from keyboards import (
    persistent_menu_keyboard,
    source_decision_keyboard,
    dest_decision_keyboard,
)

# States
STATE_SOURCE_WAIT    = 1
STATE_SOURCE_CONFIRM = 2
STATE_DEST_WAIT      = 3

async def start_add_source(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(add_source_msg)
    return STATE_SOURCE_WAIT

async def receive_source(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    context.user_data['source_candidate'] = user_input
    await update.message.reply_text(check_source)
    try:
        chat = await context.bot.get_chat(user_input)
    except BadRequest:
        await update.message.reply_text(
            error_add_source,
            reply_markup=persistent_menu_keyboard()
        )
        return ConversationHandler.END

    await update.message.reply_text(
        f"کانال «{chat.title}» با شناسه `{chat.id}` پیدا شد.",
        reply_markup=source_decision_keyboard(),
        parse_mode="Markdown"
    )
    return STATE_SOURCE_CONFIRM

async def source_decision_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data
    user_id = str(query.from_user.id)
    username = query.from_user.username or query.from_user.full_name

    recs = context.application.bot_data.setdefault('user_records', {})
    user_rec = recs.setdefault(user_id, {'username': username, 'sources': [], 'dests': []})

    if choice == "confirm_source":
        src = context.user_data['source_candidate']
        user_rec['sources'].append(src)
        await query.message.reply_text(add_source_done, reply_markup=persistent_menu_keyboard())
    else:
        await query.message.reply_text(start_msg, reply_markup=persistent_menu_keyboard())

    return ConversationHandler.END

async def start_add_dest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(add_destination_msg)
    return STATE_DEST_WAIT

    
async def receive_dest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    context.user_data['dest_candidate'] = user_input

    # Inform user we’re checking existence
    await update.message.reply_text(check_dest_sub)

    # 1) Check the channel exists
    try:
        chat = await context.bot.get_chat(user_input)
    except BadRequest:
        await update.message.reply_text(
            error_add_dest,
            reply_markup=persistent_menu_keyboard()
        )
        return ConversationHandler.END

    # 2) Check the bot’s membership/admin status
    is_admin = False
    try:
        bot_member = await context.bot.get_chat_member(chat.id, context.bot.id)
        if bot_member.status in ("administrator", "creator"):
            is_admin = True
    except BadRequest:
        # Bot cannot fetch member list → not admin
        is_admin = False

    # 3) Respond accordingly
    if is_admin:
        # Record and confirm
        user_id = str(update.effective_user.id)
        username = update.effective_user.username or update.effective_user.full_name
        recs = context.application.bot_data.setdefault('user_records', {})
        user_rec = recs.setdefault(user_id, {'username': username, 'sources': [], 'dests': []})
        user_rec['dests'].append(user_input)

        await update.message.reply_text(
            add_dest_done,
            reply_markup=persistent_menu_keyboard()
        )
    else:
        # Not admin → error and back to main
        await update.message.reply_text(
            error_user_sub,
            reply_markup=persistent_menu_keyboard()
        )

    return ConversationHandler.END
# async def receive_dest(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_input = update.message.text.strip()
#     context.user_data['dest_candidate'] = user_input
#     await update.message.reply_text(check_dest_sub)
#     try:
#         chat = await context.bot.get_chat(user_input)
#     except BadRequest:
#         await update.message.reply_text(
#             error_add_dest,
#             reply_markup=persistent_menu_keyboard()
#         )
#         return ConversationHandler.END

#     bot_member = await context.bot.get_chat_member(chat.id, context.bot.id)
#     user_id = str(update.effective_user.id)
#     username = update.effective_user.username or update.effective_user.full_name

#     recs = context.application.bot_data.setdefault('user_records', {})
#     user_rec = recs.setdefault(user_id, {'username': username, 'sources': [], 'dests': []})

#     if bot_member.status in ("administrator", "creator"):
#         user_rec['dests'].append(user_input)
#         await update.message.reply_text(add_dest_done, reply_markup=persistent_menu_keyboard())
#     else:
#         await update.message.reply_text(error_user_sub, reply_markup=persistent_menu_keyboard())

#     return ConversationHandler.END

async def show_chapar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    recs = context.application.bot_data.get('user_records', {})
    user_rec = recs.get(user_id)

    if not user_rec or (not user_rec['sources'] and not user_rec['dests']):
        await update.message.reply_text(
            "لطفا اول کانال مبدا و مقصد را در ربات تنظیم کنید",
            reply_markup=persistent_menu_keyboard()
        )
        return

    text = ["🗂 فهرست چاپار شما:"]
    if user_rec['sources']:
        text.append("\n📥 منابع:")
        for s in user_rec['sources']:
            text.append(f"• {s}")
    if user_rec['dests']:
        text.append("\n📤 مقاصد:")
        for d in user_rec['dests']:
            text.append(f"• {d}")

    await update.message.reply_text("\n".join(text), reply_markup=persistent_menu_keyboard())
