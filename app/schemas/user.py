from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(index=True)
    email: str = Field(index=True)


class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=128)


class UserRead(UserBase):
    id: int


class UserLogin(SQLModel):
    """登录一般只需要账号和密码，不必同时传用户名和邮箱。"""

    username: str
    password: str
    remember_me: bool = False


class UserInDB(UserBase):
    """只供后端内部使用，不能作为接口返回。"""

    id: int
    hashed_password: str