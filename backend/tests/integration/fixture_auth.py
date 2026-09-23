import httpx
import pytest

from datetime import datetime, timedelta, timezone
import jwt

from services.user_service.core.config import JWT_SECRET, JWT_ALGORITHM
import uuid


email = f"body_test_{uuid.uuid4().hex}@example.com"


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


def test_users_me_requires_authentication():
    response = httpx.get(
        "http://127.0.0.1:8000/api/users/me"
    )

    assert response.status_code == 401


def test_users_me_rejects_invalid_token():
    response = httpx.get(
        "http://127.0.0.1:8000/api/users/me",
        headers={
            "Authorization": "Bearer invalid-token"
        }
    )

    assert response.status_code == 401


def test_users_me_accepts_valid_token(access_token):
    response = httpx.get(
        "http://127.0.0.1:8000/api/users/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200

def test_users_me_reject_expired_token():
    now = datetime.now(timezone.utc)

    expired_token = jwt.encode(
        {
            "sub": "6",
            "iat": now - timedelta(minutes=2),
            "exp": now - timedelta(minutes=1),
        },
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

    response = httpx.get(
        "http://127.0.0.1:8000/api/users/me",
        headers={
            "Authorization": f"Bearer {expired_token}"
        }
    )

    assert response.status_code == 401


# Unknown service

def test_unknown_service_requires_authentication():
    response = httpx.get(
        "http://127.0.0.1:8000/api/orders"
    )

    assert response.status_code == 401


def test_unknown_service_returns_404(access_token):
    response = httpx.get(
        "http://127.0.0.1:8000/api/orders",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 404

def test_dynamic_user_path(access_token):
    response = httpx.get(
        "http://127.0.0.1:8000/api/users/25",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200

# dynamic path


def test_dynamic_user_path_another_id(access_token):
    response = httpx.get(
        "http://127.0.0.1:8000/api/users/99",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["id"] == 99

    #query parameter limit test


def test_query_parameter_forwarding(access_token):
    response = httpx.get(
        "http://127.0.0.1:8000/api/users/test?limit=25",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["limit"] == 25


    # header forwarding

def test_authorization_header_forwarding(access_token):
    response = httpx.get(
        "http://127.0.0.1:8000/api/users/me",

    headers={
        "Authorization":f"Bearer {access_token}"
    }
    )

    assert response.status_code == 200

#  gateway can received json body and successful forward to post/auth /register
def test_post_body_forwarding():
    email = f"body_test_{uuid.uuid4().hex}@example.com"

    response = httpx.post(
        "http://127.0.0.1:8000/api/auth/register",
        json={
            "name": "Body Test User",
            "email": email,
            "password": "Test@12345"
        }
    )

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == "Body Test User"
    assert data["email"] == email