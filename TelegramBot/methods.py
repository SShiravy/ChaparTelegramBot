from telegram import Bot
from config import settings
import logging


async def send_message_to_chat(message, chat_id):
    try:
        bot = Bot(settings.TELEGRAM_BOT_TOKEN)
        if message.photo:
            await bot.send_photo(
                chat_id, message.photo.file_id, caption=message.caption
            )
        elif message.video:
            await bot.send_video(
                chat_id, message.video.file_id, caption=message.caption
            )
        elif message.animation:
            await bot.send_animation(
                chat_id, message.animation.file_id, caption=message.caption
            )
        elif message.document:
            await bot.send_document(
                chat_id, message.document.file_id, caption=message.caption
            )
        elif message.sticker:
            await bot.send_sticker(
                chat_id,
                message.sticker.file_id,
            )
        elif message.web_page:
            await bot.send_message(chat_id, message.text + message.web_page.url)
        else:
            await bot.send_message(chat_id, message.text)

        logging.info(f"msg to chat id:{chat_id} sent successfully!")
        return True
    except Exception as e:
        logging.error(f"sending msg {message} to chat {chat_id} failed: {e}")
    return False
