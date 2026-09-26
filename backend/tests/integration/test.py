import httpx
import pytest


@pytest.fixture
def access_token():
    response = httpx.post(
        "http://127.0.0.1:8000/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "Test@12345"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]