from account_bot import DeliveryBot
from ..config import settings

def run_account_bot():
    account_bot = DeliveryBot("main_delivery_bot",settings.USER_BOT_STR_SESSION)
    while True:
        # TODO: get n as Number of recorded data in Delivery tabel
        # TODO: for loop on n and get each record
        # TODO: 

        
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
