from fastapi import Depends, HTTPException, status

from services.user_service.core.dependencies import get_current_user
from services.user_service.database import models


def require_admin(
    current_user: models.User = Depends(get_current_user)
):
    # Authentication has already happened through get_current_user().
    # This function is responsible only for authorization.
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user