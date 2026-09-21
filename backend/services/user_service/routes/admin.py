from fastapi import APIRouter, Depends

from services.user_service.core.authorization import require_admin
from services.user_service.database import models


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/test")
def admin_test(
    current_user: models.User = Depends(require_admin)
):
    # This endpoint can only be reached by authenticated
    # users whose role is "admin".
    return {
        "message": "Admin access granted",
        "user_id": current_user.id,
        "role": current_user.role
    }