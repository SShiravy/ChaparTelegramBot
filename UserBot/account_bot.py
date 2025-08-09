from pyrogram.client import Client
from ..Models.delivery import Delivery
from custom_logger import logger


class DeliveryBot:
    def __init__(self,name:str, session_str):
        self.bot = Client(name=name, in_memory=True,session_string=session_str)
    
    async def join_chat(self,chat_id) -> bool:
        """
        chat_id can be:
            - "@username"
            - "https://t.me/joinchat/xxxx"
            - "-1001234567890" (if bot session already recognized)
        """

        try:
            chat = await self.bot.join_chat(chat_id)
            logger.info(f" account bot joined: {chat.title} ({chat.id})")
            return True
        except Exception as e:
            logger.error(f" account bot Failed to join {chat_id}: {e}")
            return False

    async def get_last_msg_id(self,chat_id)->int|None:
        try:
            async for message in self.bot.get_chat_history(chat_identifier, limit=1): # type:ignore
                logger.info(f"Last message ID in {chat_id}: {message.id}")
                return message.id
            logger.warning(f"No messages found in {chat_id}")
            return None
        except Exception as e:
            logger.error(f"account bot Failed to get last message from {chat_id}: {e}")
            return None

    async def run(self,coro):
        self.bot.run(coro)
  
    