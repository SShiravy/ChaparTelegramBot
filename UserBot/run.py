from account_bot import DeliveryBot
from ..config import settings
from sqlmodel import Session, select
from Database.database import engine
from Models.delivery import Delivery
from custom_logger import logger
import asyncio


async def polling_loop(account_bot):
    while True:
        await asyncio.sleep(3)
        number_of_delivery = 10
        # TODO: get n as Number of recorded data in Delivery tabel
        for delivery_id in range(1,number_of_delivery+1):
            with Session(engine) as db_session:
                selected_delivery = db_session.exec(
                    select(Delivery).where(Delivery.id == delivery_id)).one()
                
                # if selected_delivery is a new recorded delivery then it will be None
                if selected_delivery.account_bot_joined_source == None:
                    
                    # Join to source chat for getting new msgs
                    joined = await account_bot.join_chat(selected_delivery.source_id)
                    if joined == False:
                        continue
                    selected_delivery.account_bot_joined_source = True
                    
                    # Get last forwarded msg id to forward just new msgs
                    recived_last_msg_id = await account_bot.get_last_msg_id(selected_delivery.source_id)
                    if recived_last_msg_id == None:
                        continue
                    selected_delivery.last_forwarded_msg_id = recived_last_msg_id

                    # Update delivery record so it will check for new msgs and forward them
                    update_delivery_in_db(db_session,selected_delivery)

                else:
                    selected_last_msg_id = selected_delivery.last_forwarded_msg_id
                    async for msg in account_bot.bot.get_chat_history(selected_delivery.source_id,limit=100):  # type:ignore
                        if msg.id <= selected_last_msg_id:
                            break
                        # TODO: forward message to destination chat using Telegram BOT

def update_delivery_in_db(db_session,delivery:Delivery) -> bool:
    try:
        db_session.add(delivery)
        db_session.commit()
        db_session.refresh(delivery)
        logger.info(f"update delivery:{delivery} in database")
    except Exception as e:
        logger.error(f"error on updating delivery:{delivery} to database, error:{e}")
        return False
    return True
        

if __name__ == "__main__":
    account_bot = DeliveryBot("main_delivery_bot",settings.USER_BOT_STR_SESSION)
    account_bot.run(polling_loop(account_bot))
    # TODO: it is so badddddddd to do this but i don't know how to fix it yet


# async def polling_loop():
#     async with user_bot:
#         await set_last_msg_ids()
#         while True:
#             for channel_id in source_channel_id:
#                 # try:
#                 last_msg = all_channels_last_msg_id.get(channel_id,100)
#                 async for msg in user_bot.get_chat_history(channel_id, limit=100): # type:ignore
#                     if msg.id > last_msg:
#                         print(msg)
#                         print('last msg id:',last_msg,'text:',msg.text)
#                         await handle_message(msg,channel_id)
#                 # except Exception as e:
#                 #     print(f"⚠️ Error reading from {channel_id}:", e)
#             print('sleep for next turn')
#             await asyncio.sleep(3)
