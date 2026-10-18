from sqlmodel import create_engine, SQLModel
from config import settings

# engine = create_engine(settings.PostgreSQL_DB_URL + settings.PostgreSQL_DB_NAME)

sqlite_url = f"sqlite:///{settings.DATABASE_NAME}"
engine = create_engine(sqlite_url, echo=False)


def create_tables():
    # Import All models here to Create Tables
    from Models.delivery import Delivery
    from Models.user import User

    SQLModel.metadata.create_all(engine)
