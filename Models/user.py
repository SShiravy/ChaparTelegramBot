from sqlmodel import SQLModel, Field
from enum import Enum
import datetime

class UserType(Enum):
    SUPERUSER = 'superuser'
    CUSTOMER = 'customer'
    FRIEND = 'friend'

class User(SQLModel,table=True):
    __tablename__ = 'users' # type: ignore
    id: int | None = Field(default=None, primary_key=True)
    account_id: str = Field(unique=True)
    username: str|None = Field(default=None)
    user_type: UserType = Field(default=UserType.CUSTOMER)
    premium: bool = Field(default=False)
    premium_exp_time: datetime.date | None = Field(default=None)
    n_delivery: int = Field(default=0) 
