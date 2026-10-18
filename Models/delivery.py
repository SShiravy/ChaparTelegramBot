from sqlmodel import SQLModel, Field


class Delivery(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default="-", max_length=50, index=True)
    user_account_id: str = Field(foreign_key="users.account_id", index=True)
    source_id: str = Field(..., index=True)
    source_name: str | None = Field(default=None)
    destination_id: str = Field(...)
    destination_name: str | None = Field(default=None)
    active: bool = Field(default=True)
    last_forwarded_msg_id: int | None = Field(default=None)
    n_forwarded_msg: int = Field(default=0)
    account_bot_joined_source: bool = Field(default=False)
