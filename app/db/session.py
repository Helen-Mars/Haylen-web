"""数据库连接与会话管理"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import Session

from app.core.config import settings


# ── 数据库引擎 ──────────────────────────────────────────────────────────
connect_args = {"check_same_thread": False}
engine = create_engine(settings.database_url, connect_args=connect_args)


# ── Session 依赖注入 ─────────────────────────────────────────────────────
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
