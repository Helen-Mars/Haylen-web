from typing import Literal

from sqlmodel import Field, SQLModel


class ChatRequest(SQLModel):
    message: str = Field(min_length=1, max_length=5000)
    model: Literal["gpt-4o-mini"] = "gpt-4o-mini"