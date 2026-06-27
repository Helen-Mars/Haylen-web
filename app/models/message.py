from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Message(SQLModel, table=True):
    """留言数据库表。"""

    __tablename__ = "message"

    id: int | None = Field(default=None, primary_key=True)

    # 当前留言回复的是哪一条留言；顶级留言时为 None
    parent_id: int | None = Field(
        default=None,
        foreign_key="message.id",
    )

    name: str
    title: str
    content: str

    create_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    is_approved: bool = Field(default=False)