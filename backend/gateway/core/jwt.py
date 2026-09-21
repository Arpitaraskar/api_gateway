from fastapi import HTTPException,status
import jwt

from gateway.core.config import (
    JWT_SECRET,
    JWT_ALGORITHM
)

def verify_access_token(token:str)-> dict:
    """
    Verify a JWT received by the Gateway.

    The Gateway uses the same secret and algorithm
    as the User Service, but keeps its own JWT logic.
    """

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

    except jwt.InvalidTokenError as error:
       print("JWT VERIFICATION ERROR:", type(error).__name__)
       print("JWT VERIFICATION MESSAGE:", str(error))

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication token"
    )