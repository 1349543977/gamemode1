import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_wechat_login():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/wechat-login",
            json={"code": "test_code_123", "platform": "wechat"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data


@pytest.mark.asyncio
async def test_get_profile():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        login_resp = await client.post(
            "/api/v1/auth/wechat-login",
            json={"code": "test_profile", "platform": "wechat"},
        )
        token = login_resp.json()["access_token"]

        response = await client.get(
            "/api/v1/auth/profile",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "nickname" in data
