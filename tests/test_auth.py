"""认证相关接口测试"""

import pytest
from httpx import AsyncClient

PREFIX = "/api/v1"


@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient):
    """测试用户注册成功"""
    response = await client.post(
        f"{PREFIX}/authing/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password" not in data


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """测试登录成功"""
    await client.post(
        f"{PREFIX}/authing/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "loginpass123",
        },
    )

    response = await client.post(
        f"{PREFIX}/authing/login",
        json={
            "username": "loginuser",
            "password": "loginpass123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert data["user"]["username"] == "loginuser"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """测试错误密码登录"""
    await client.post(
        f"{PREFIX}/authing/register",
        json={
            "username": "wrongpw",
            "email": "wrongpw@example.com",
            "password": "correctpass",
        },
    )

    response = await client.post(
        f"{PREFIX}/authing/login",
        json={
            "username": "wrongpw",
            "password": "wrongpass",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_user_not_found(client: AsyncClient):
    """测试不存在的用户登录"""
    response = await client.post(
        f"{PREFIX}/authing/login",
        json={
            "username": "nobody",
            "password": "somepass",
        },
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_dashboard_requires_auth(client: AsyncClient):
    """测试未认证访问 /dashboard"""
    response = await client.get(f"{PREFIX}/authing/dashboard")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_users_me_requires_auth(client: AsyncClient):
    """测试未认证访问 /users/me"""
    response = await client.get(f"{PREFIX}/authing/users/me")
    assert response.status_code == 401

