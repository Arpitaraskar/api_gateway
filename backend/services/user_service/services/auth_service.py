from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from services.user_service.database import models
from services.user_service.core.security import (
    hash_password,
    verify_password
)
from services.user_service.core.jwt import create_access_token
from services.user_service.schemas.user import UserUpdate


def register_user(
    user_data,
    db: Session
):
    # Check whether an account with this email already exists.
    existing_user = db.query(models.User).filter(
        models.User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password before storing the user.
    # Plain-text passwords must never be stored in the database.
    hashed_password = hash_password(user_data.password)

    # The role is intentionally NOT taken from user_data.
    # Every public registration creates a normal user.
    new_user = models.User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password,
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(
    user_data,
    db: Session
):
    # Find the account using the email supplied during login.
    existing_user = db.query(models.User).filter(
        models.User.email == user_data.email
    ).first()

    # Use the same error for an unknown email and wrong password.
    # This prevents revealing whether an email is registered.
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Compare the supplied password against the stored password hash.
    if not verify_password(
        user_data.password,
        existing_user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create a JWT containing the authenticated user's ID.
    access_token = create_access_token(
        user_id=str(existing_user.id)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# update user --email,name


def update_current_user(
    current_user: models.User,
    user_data: UserUpdate,
    db: Session
) -> models.User:

    if user_data.name is not None:
        current_user.name = user_data.name

    if user_data.email is not None:
        existing_user = (
            db.query(models.User)
            .filter(
                models.User.email == user_data.email,
                models.User.id != current_user.id
            )
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        current_user.email = user_data.email

    db.commit()
    db.refresh(current_user)

    return current_user