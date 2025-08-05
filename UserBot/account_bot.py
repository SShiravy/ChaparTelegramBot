from pyrogram.client import Client
from ..Models.delivery import Delivery
from sqlmodel import Session
from ..Database.database import engine
class DeliveryBot:
    def __init__(self,name:str, session_str):
        self.bot = Client(name=name, in_memory=True,session_string=session_str)
    
    async def handle_forward(self,msg,delivery:Delivery,db_session:Session):
        await self.bot.forward_messages(
            chat_id=delivery.destination_id,
            from_chat_id=delivery.source_id,
            message_ids=msg.id,
        )
        if msg.id > delivery.last_forwarded_msg_id:
            delivery.last_forwarded_msg_id = msg.id
            delivery.n_forwarded_msg += 1
            db_session.add(delivery)
            db_session.commit()
        # TODO: add multiple forward support
        # TODO: add error handling
        

    async def set_last_msg_ids(self):
        with self.bot:
            for channel_id in source_channel_id:
                async for msg in user_bot.get_chat_history(channel_id, limit=1): # type:ignore
                    all_channels_last_msg_id[channel_id] = msg.id
        print(all_channels_last_msg_id)
        
async def handle_message(msg, channel_id):
    global all_channels_last_msg_id

    if msg.id > all_channels_last_msg_id[channel_id]:
        all_channels_last_msg_id[channel_id] = msg.id 

    if signal_filter(msg, channel_id):
        await user_bot.forward_messages(
            chat_id=target_channel_id,
            from_chat_id=msg.chat.id,
            message_ids=msg.id,
        )


