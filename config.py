from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    def __new__(cls):
        if not hasattr(cls, "__instance__"):
            cls.__instance__ = object.__new__(cls)
        return cls.__instance__

    # Database
    DATABASE_NAME: str
    # TelegramBot
    TELEGRAM_BOT_TOKEN: str
    # UserBot
    USER_BOT_API_ID: int
    USER_BOT_API_HASH: str
    USER_BOT_STR_SESSION: str
    USER_BOT_USE_PROXY: bool
    USER_BOT_SLEEP_TIME: int


    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore