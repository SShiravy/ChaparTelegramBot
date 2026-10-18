from Database.database import create_tables
from TelegramBot.bot import start_telegram_bot
from custom_logger import ConfigRootLogger
import logging


ConfigRootLogger(
    consol_log_level=logging.DEBUG,
    log_file=True,
    file_log_level=logging.DEBUG,
    file_log_name="TelegramBot",
)


if __name__ == "__main__":
    create_tables()
    while True:
        try:
            start_telegram_bot()
        except Exception as e:
            logging.error(e)
