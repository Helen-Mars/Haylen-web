"""分析统计相关接口测试"""

import pytest
from httpx import AsyncClient

PREFIX = "/api/v1/analyzing"


@pytest.mark.asyncio
async def test_track_page(client: AsyncClient):
    """测试页面访问统计"""
    response = await client.get(f"{PREFIX}/track_page", params={"url": "/"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Page view recorded"


@pytest.mark.asyncio
async def test_page_view_count_initial(client: AsyncClient):
    """测试初始页面访问计数"""
    response = await client.get(f"{PREFIX}/page_view_count")
    assert response.status_code == 200
    data = response.json()
    assert "total_views" in data
    assert data["total_views"] >= 0


@pytest.mark.asyncio
async def test_page_view_increment(client: AsyncClient):
    """测试页面访问计数递增"""
    # 获取当前计数
    resp_before = await client.get(f"{PREFIX}/page_view_count")
    count_before = resp_before.json()["total_views"]

    # 触发一次访问
    await client.get(f"{PREFIX}/track_page", params={"url": "/test"})

    # 获取新计数
    resp_after = await client.get(f"{PREFIX}/page_view_count")
    count_after = resp_after.json()["total_views"]

    assert count_after == count_before + 1
