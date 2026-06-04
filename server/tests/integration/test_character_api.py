import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_create_character():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        login_resp = await client.post(
            "/api/v1/auth/wechat-login",
            json={"code": "test_char_create", "platform": "wechat"},
        )
        token = login_resp.json()["access_token"]

        response = await client.post(
            "/api/v1/characters",
            json={"name": "张三", "gender": "male", "city_id": 1},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "张三"
        assert data["age"] == 0
        assert data["stage"] == "infant"
        assert data["is_alive"] is True
        assert "stats" in data


@pytest.mark.asyncio
async def test_get_character():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        login_resp = await client.post(
            "/api/v1/auth/wechat-login",
            json={"code": "test_char_get", "platform": "wechat"},
        )
        token = login_resp.json()["access_token"]

        create_resp = await client.post(
            "/api/v1/characters",
            json={"name": "李四", "gender": "female", "city_id": 1},
            headers={"Authorization": f"Bearer {token}"},
        )
        char_id = create_resp.json()["id"]

        response = await client.get(
            f"/api/v1/characters/{char_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["name"] == "李四"


@pytest.mark.asyncio
async def test_get_character_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        login_resp = await client.post(
            "/api/v1/auth/wechat-login",
            json={"code": "test_char_notfound", "platform": "wechat"},
        )
        token = login_resp.json()["access_token"]

        response = await client.get(
            "/api/v1/characters/99999",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404
