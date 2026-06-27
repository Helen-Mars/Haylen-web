from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class PageView(SQLModel, table=True):
    """全站浏览量统计表。"""

    __tablename__ = "page_views"

    id: int | None = Field(default=None, primary_key=True)
    count: int = Field(default=0)

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )