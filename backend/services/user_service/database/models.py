from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from services.user_service.database.database import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100)
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True, #Two users cannot have the same email
        index=True    # makes searching faster
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255)
    )

     # Defines the user's authorization level.
    #
    # "user" is the default so newly registered accounts
    # cannot accidentally receive administrative privileges.
    role: Mapped[str] = mapped_column(
        String(20),
        default="user",
        nullable=False  # role cannot be empty,Must have a value
    )