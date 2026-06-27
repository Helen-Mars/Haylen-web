"""测试配置与夹具"""

from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

from app.api.router import api_router
from app.db.session import get_session
from app.web.router import web_router

# ── 测试数据库 ──────────────────────────────────────────────────────────
TEST_DB = "sqlite:///./tests/test.db"
connect_args = {"check_same_thread": False}
_test_engine = create_engine(TEST_DB, connect_args=connect_args)


def override_get_session():
    with Session(_test_engine) as session:
        yield session


def _health_check():
    return {"status": "ok", "version": "1.0.0"}


@pytest.fixture(autouse=True)
def setup_db():
    """每个测试函数前重建表"""
    SQLModel.metadata.create_all(_test_engine)
    yield
    SQLModel.metadata.drop_all(_test_engine)


@pytest.fixture(name="app")
def app_fixture() -> FastAPI:
    app = FastAPI()

    # 注册路由
    app.include_router(api_router)
    app.include_router(web_router)

    # 健康检查
    app.add_api_route("/health", _health_check, methods=["GET"], tags=["System"])

    # 替换数据库依赖
    app.dependency_overrides[get_session] = override_get_session

    return app


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
