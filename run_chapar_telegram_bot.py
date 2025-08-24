from Database.database import create_tables
from TelegramBot.bot import run_telegram_bot


if __name__ == '__main__':
    create_tables()
    run_telegram_bot()
