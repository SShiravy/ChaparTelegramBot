from UserBot.account_bot import DeliveryBot
from config import settings
from custom_logger import ConfigRootLogger
from UserBot.user_bot_loop import start_user_bot
import logging


ConfigRootLogger(consol_log_level=logging.DEBUG,log_file=True,
                 file_log_level=logging.DEBUG, file_log_name='AccountBot')



if __name__ == "__main__":
    user_bot = DeliveryBot("main_delivery_bot",
                            settings.USER_BOT_STR_SESSION,
                            use_proxy=settings.USER_BOT_USE_PROXY)    

    user_bot.bot.run(start_user_bot(user_bot))

