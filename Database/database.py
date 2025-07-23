from sqlmodel import create_engine, SQLModel
from ..config import settings

engine = create_engine(settings.PostgreSQL_DB_URL + settings.PostgreSQL_DB_NAME)

def create_tables():
    SQLModel.metadata.create_all(engine)
