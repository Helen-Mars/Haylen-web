"""留言相关接口测试"""

import pytest
from httpx import AsyncClient

PREFIX = "/api/v1/messaging"



@pytest.mark.asyncio
async def test_post_message_success(client: AsyncClient):
    """测试发布留言成功"""
    response = await client.post(
        f"{PREFIX}/messages",
        json={
            "name": "Test User",
            "title": "A Test Message",
            "content": "x" * 100,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "waiting_approval"


@pytest.mark.asyncio
async def test_post_message_invalid_content_too_short(client: AsyncClient):
    """测试留言内容过短"""
    response = await client.post(
        f"{PREFIX}/messages",
        json={
            "name": "Test",
            "title": "Test",
            "content": "short",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_post_message_with_parent(client: AsyncClient):
    """测试回复留言"""
    parent_resp = await client.post(
        f"{PREFIX}/messages",
        json={
            "name": "Parent",
            "title": "Parent",
            "content": "x" * 100,
        },
    )
    parent_id = parent_resp.json().get("id")

    response = await client.post(
        f"{PREFIX}/messages",
        json={
            "name": "Child",
            "title": "Reply",
            "content": "y" * 100,
            "parent_id": parent_id,
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_approve_message_not_found(client: AsyncClient):
    """测试审批不存在的留言"""
    response = await client.post(f"{PREFIX}/admin/approve/99999")
    assert response.status_code == 404
