from datetime import datetime
from unittest.mock import patch, AsyncMock

from src.services.auth import auth_service


def test_get_contacts(client, get_token, monkeypatch):
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/contacts", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 0


def test_create_contact(client, get_token, monkeypatch):
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("api/contacts",
                               json={"first_name": "test", "last_name": "test", "email": "test@email.com",
                                     "phone_number": "+123456789", "description": "test",
                                     "birthday": str(datetime.now().date())}, headers=headers)
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["first_name"] == "test"
        assert data["last_name"] == "test"
        assert data["email"] == "test@email.com"
        assert data["phone_number"] == "+123456789"
        assert data["description"] == "test"
        assert data["birthday"] == str(datetime.now().date())
