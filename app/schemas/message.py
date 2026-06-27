from datetime import datetime

from sqlmodel import Field, SQLModel


class MessageCreate(SQLModel):
    name: str = Field(
        min_length=1,
        max_length=50,
        description="name, 1-50 characters",
    )
    title: str = Field(
        min_length=1,
        max_length=100,
        description="title, 1-100 characters",
    )
    content: str = Field(
        min_length=100,
        max_length=1000,
        description="content, 100-1000 characters",
    )
    parent_id: int | None = None


class MessageRead(SQLModel):
    id: int
    parent_id: int | None
    name: str
    title: str
    content: str
    created_at: datetime
    is_approved: bool