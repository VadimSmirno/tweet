import pytest
from app.app import app
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_add_user():
    client = TestClient(app)
    user_data = {
        "name": "Test User",
        "email": "test@example.com",

    }
    response = await client.post("/api/users", json=user_data)
    assert response.status_code == 200
    user = response.json()
    assert "id" in user
    assert user["name"] == "Test User"


@pytest.mark.asyncio
async def test_get_all_users():
    client = TestClient(app)
    response = await client.get("/api/users")
    assert response.status_code == 200
    users = response.json()
    assert len(users) > 0


@pytest.mark.asyncio
async def test_get_users_profile():
    client = TestClient(app)
    api_key = "test"
    response = await client.get("/api/users/me", headers={"api_key": api_key})
    assert response.status_code == 200
    result = response.json()
    assert result["result"] is True
    assert "user" in result


@pytest.mark.asyncio
async def test_get_users_profile_by_id():
    client = TestClient(app)
    api_key = "test"
    user_id = 1
    response = await client.get(f"/api/users/{user_id}", headers={"api_key": api_key})
    assert response.status_code == 200
    result = response.json()
    assert result["result"] is True
    assert "user" in result


@pytest.mark.asyncio
async def test_add_new_follower():
    client = TestClient(app)
    api_key = "test"
    user_id = 1
    response = await client.post(f"/api/users/{user_id}/follow", headers={"api_key": api_key})
    assert response.status_code == 200
    result = response.json()
    assert result["result"] is True


@pytest.mark.asyncio
async def test_add_new_tweet():
    client = TestClient(app)
    api_key = "test"
    new_tweet_data = {
        "tweet_data": "Test tweet content",
        "tweet_media_ids": [1]
    }
    response = await client.post("/api/tweets", json=new_tweet_data, headers={"api_key": api_key})
    assert response.status_code == 200
    result = response.json()
    assert result["result"] is True
    assert "tweet_id" in result


@pytest.mark.asyncio
async def test_delete_follower():
    client = TestClient(app)
    api_key = "test"
    user_id = 1
    response = await client.delete(f"/api/users/{user_id}/follow", headers={"api_key": api_key})
    assert response.status_code == 200
    result = response.json()
    assert result["result"] is True


@pytest.mark.asyncio
async def test_delete_tweet():
    client = TestClient(app)
    api_key = "test"
    tweet_id = 1
    response = await client.delete(f"/api/tweets/{tweet_id}", headers={"api_key": api_key})
    assert response.status_code == 200
    result = response.json()
    assert result["result"] is True


