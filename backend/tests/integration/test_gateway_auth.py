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
            "Authorization":"Bearer invalid-token"
        }
    )

    assert response.status_code == 401

    