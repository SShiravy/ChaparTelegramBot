from pyrogram.client import Client
from UserBot.proxy_setting import get_proxy_settings
import logging


class DeliveryBot:
    def __init__(self, name: str, session_str, use_proxy=False):
        proxy = None
        if use_proxy:
            proxy = get_proxy_settings()

        self.bot = Client(
            name=name, in_memory=True, session_string=session_str, proxy=proxy
        )  # type: ignore

    @classmethod
    async def generate_str_session(
        cls, api_id: int, api_hash: str, use_proxy=False
    ) -> str:
        """Login with phone and return a session string"""
        try:
            proxy = None
            if use_proxy:
                proxy = get_proxy_settings()
            async with Client(
                "session_generator", api_id=api_id, api_hash=api_hash, proxy=proxy
            ) as app:  # type: ignore
                session_string = await app.export_session_string()
                logging.debug(f"Generated session string: {session_string}")
            return session_string
        except Exception as e:
            logging.error(f"Failed to generate session string: {e}")
            return ""

    async def join_chat(self, chat_id) -> bool:
        """
        chat_id can be:
            - "@username"
            - "https://t.me/joinchat/xxxx"
            - "-1001234567890" (if bot session already recognized)
        """

        try:
            async with self.bot:
                chat = await self.bot.join_chat(chat_id)
                logging.info(f" account bot joined: {chat.title} ({chat.id})")
            return True
        except Exception as e:
            logging.error(f" account bot Failed to join {chat_id}: {e}")
            return False

    async def get_last_msg_id(self, chat_id) -> int | None:
        msg_id = None
        try:
            async with self.bot:
                async for message in self.bot.get_chat_history(chat_id, limit=1):  # type:ignore
                    logging.debug(f"Last message ID in {chat_id}: {message.id}")
                    msg_id = message.id
            if msg_id:
                return msg_id
            logging.warning(f"No messages found in {chat_id}")
            return None
        except Exception as e:
            logging.error(f"account bot Failed to get last message from {chat_id}: {e}")
            return None

    async def get_chat_history(self, chat_id, limit: int = 100):
        try:
            async with self.bot:
                async for message in self.bot.get_chat_history(chat_id, limit):  # type:ignore
                    logging.debug(f"msg id:{message.id}")
                    yield message
        except Exception as e:
            logging.error(f"account bot Failed to get chat history from {chat_id}: {e}")

    async def get_chat_numerical_id(self, chat_id: str):
        try:
            async with self.bot:
                chat = await self.bot.get_chat(chat_id)
                logging.debug(f"numerical id from {chat_id} fetched as {chat.id}")  # type: ignore
            return chat.id  # type: ignore
        except Exception as e:
            logging.error(f"getting chat numerical id from {chat_id} failed: {e}")
