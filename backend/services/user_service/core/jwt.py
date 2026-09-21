#core/jwt.py
from datetime import datetime, timedelta, timezone

import jwt

from fastapi import HTTPException, status

from services.user_service.core.config import (
    JWT_SECRET,
    JWT_ALGORITHM,
    JWT_EXPIRATION_MINUTES
)


def create_access_token(
    user_id: str,
    extra_data: dict | None = None
) -> str:

    payload = extra_data.copy() if extra_data else {}

    # Every access token must identify its subject.
    payload["sub"] = user_id

    now = datetime.now(timezone.utc)

    expire = now + timedelta(
        minutes=JWT_EXPIRATION_MINUTES
    )

    # TEMPORARY: create an already-expired token for testing.
    #expire = now - timedelta(minutes=1)

    payload["iat"] = now
    payload["exp"] = expire

    token = jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

    return token

def verify_access_token(token: str) -> dict:
    try:
        # Decode the token using the same secret and algorithm
        # that were used when the token was created.
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )

        # Every access token must contain the user's ID.
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )

        return payload

    except jwt.ExpiredSignatureError:
        # The token's "exp" time has passed.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired"
        )

    except jwt.InvalidTokenError:
        # The signature, structure, algorithm, or other token data is invalid.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )