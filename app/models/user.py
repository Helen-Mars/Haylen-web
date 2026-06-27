from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """用户数据库表。"""

    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str