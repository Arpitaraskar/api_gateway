# import httpx
# import pytest

# def test_users_me_requires_authentication():

#     response = httpx.get(
#         "http://127.0.0.1:8000/api/users/me"
#     )

#     assert response.status_code == 401

# def test_users_me_rejects_invalid_token():
#     response = httpx.get(
#         "http://127.0.0.1:8000/api/users/me",

#         headers={
#             "Authorization":"Bearer invalid-token"
#         }
#     )


#     assert response.status_code == 401


# def test_update_user_email(access_token):
#     response = httpx.put(
#         "http://127.0.0.1:8001/users/me",
#         headers={
#             "Authorization": f"Bearer {access_token}"
#         },
#         json={
#             "email": "updated_test@example.com"
#         }
#     )

#     assert response.status_code == 200
#     assert response.json()["email"] == "updated_test@example.com"

import httpx


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


def test_update_user_through_gateway(access_token):
    email = "gateway_update@example.com"

    response = httpx.put(
        "http://127.0.0.1:8000/api/users/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "name": "Arpita Gateway Test",
            "email": email
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Arpita Gateway Test"
    assert data["email"] == email


def test_update_user_without_token():
    response = httpx.put(
        "http://127.0.0.1:8000/api/users/me",
        json={
            "name": "No Token User"
        }
    )

    assert response.status_code == 401


def test_update_user_with_invalid_token():
    response = httpx.put(
        "http://127.0.0.1:8000/api/users/me",
        headers={
            "Authorization": "Bearer invalid-token"
        },
        json={
            "name": "Invalid Token User"
        }
    )

    assert response.status_code == 401


def test_update_user_with_invalid_email(access_token):
    response = httpx.put(
        "http://127.0.0.1:8000/api/users/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "email": "not-an-email"
        }
    )

    assert response.status_code == 422


def test_update_user_name_only(access_token):
    response = httpx.put(
        "http://127.0.0.1:8000/api/users/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "name": "Name Only Test"
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Name Only Test"


def test_update_user_email_only(access_token):
    email = f"email_update_{__import__('uuid').uuid4().hex}@example.com"

    response = httpx.put(
        "http://127.0.0.1:8000/api/users/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "email": email
        }
    )

    assert response.status_code == 200
    assert response.json()["email"] == email