from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    def __new__(cls):
        if not hasattr(cls, "__instance__"):
            cls.__instance__ = object.__new__(cls)
        return cls.__instance__

    # Database
    PostgreSQL_DB_URL: str
    PostgreSQL_DB_NAME: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore