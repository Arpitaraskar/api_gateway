#core/depencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from services.user_service.core.jwt import verify_access_token
from services.user_service.database.database import get_db
from services.user_service.database import models


# HTTPBearer reads:
# Authorization: Bearer <JWT>
#
# Keeping this in one dependency means protected routes
# don't need to manually parse the Authorization header.
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    # Verify the JWT signature, expiration, and required claims.
    payload = verify_access_token(token)

    # The "sub" claim contains the authenticated user's ID.
    user_id = payload["sub"]

    # Load the actual user from the database.
    user = db.query(models.User).filter(
        models.User.id == int(user_id)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user