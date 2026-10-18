from Database.db_methods import get_all_deliveries, update_delivery_in_db
from TelegramBot.methods import send_message_to_chat
from UserBot.account_bot import DeliveryBot
from config import settings
import asyncio
from datetime import datetime
import logging


async def pre_configurations():
    if settings.USER_BOT_STR_SESSION:
        return settings.USER_BOT_STR_SESSION
    res = await DeliveryBot.generate_str_session(
        settings.USER_BOT_API_ID, settings.USER_BOT_API_HASH, use_proxy=True
    )
    settings.USER_BOT_STR_SESSION = res
    logging.info(f"str_session generated : {res}")
    return res


async def polling_loop(delivery_bot: DeliveryBot):
    all_deliveries = get_all_deliveries()
    for delivery in all_deliveries:
        if not delivery.active:
            continue
        # if selected_delivery is a new recorded delivery then it will be None
        if delivery.account_bot_joined_source is False:
            logging.info(f"new delivery detected : {delivery.name}")
            # Join to source chat for getting new msgs
            joined = await delivery_bot.join_chat(delivery.source_id)
            if joined == False:
                continue
            delivery.account_bot_joined_source = True

            # Get last forwarded msg id to forward just new msgs
            recived_last_msg_id = await delivery_bot.get_last_msg_id(delivery.source_id)
            if recived_last_msg_id == None:
                continue
            delivery.last_forwarded_msg_id = recived_last_msg_id

            # Update delivery record so it will check for new msgs and forward them
            update_delivery_in_db(delivery)
            continue

        else:
            selected_last_msg_id = delivery.last_forwarded_msg_id
            destination_id = await delivery_bot.get_chat_numerical_id(
                delivery.destination_id
            )
            msgs = delivery_bot.get_chat_history(delivery.source_id, limit=100)
            all_not_sended_msgs = []
            async for msg in msgs:
                if msg.id <= selected_last_msg_id:
                    await msgs.aclose()
                    break
                all_not_sended_msgs.append(msg)

            n_forwarded = 0
            for msg in all_not_sended_msgs[::-1]:
                sending_res = await send_message_to_chat(msg, destination_id)
                if sending_res:
                    n_forwarded += 1

            if n_forwarded > 0:
                delivery.n_forwarded_msg += n_forwarded
                delivery.last_forwarded_msg_id = all_not_sended_msgs[0].id
                update_delivery_in_db(delivery)


async def start_user_bot(delivery_bot: DeliveryBot):
    start_time = datetime.now()
    while True:
        try:
            await polling_loop(delivery_bot)
            logging.critical(
                f"total elapsed time: {str(datetime.now() - start_time)}; sleep for {settings.USER_BOT_SLEEP_TIME} seconds"
            )
            await asyncio.sleep(settings.USER_BOT_SLEEP_TIME)
        except Exception as e:
            logging.error(e)
