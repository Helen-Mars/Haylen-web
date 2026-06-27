"""健康检查测试"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """验证健康检查接口"""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


@pytest.mark.asyncio
async def test_page_view_count(client: AsyncClient):
    """验证浏览量接口可访问"""
    response = await client.get("/api/v1/analyzing/page_view_count")
    assert response.status_code == 200
    data = response.json()
    assert "total_views" in data
