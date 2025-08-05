from sqlmodel import SQLModel, Field

class Delivery(SQLModel):
    id: int = Field(default=None, primary_key=True)
    user_id: int =  Field(foreign_key="users.id")
    source_id: str = Field(...,index=True)
    source_name: str|None = Field(default=None)
    destination_id: str = Field(...)
    destination_name: str|None = Field(default=None)
    active: bool = Field(default=True)