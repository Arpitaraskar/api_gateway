from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from services.user_service.database.database import get_db
from services.user_service.schemas.user import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse
)
from services.user_service.services.auth_service import (
    register_user,
    login_user
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    # The route handles HTTP concerns.
    # The service handles the registration business logic.
    return register_user(user_data, db)


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    # The route handles HTTP concerns.
    # The service handles the login business logic.
    return login_user(user_data, db)