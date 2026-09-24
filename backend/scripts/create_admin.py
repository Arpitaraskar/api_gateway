import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from services.user_service.core.security import hash_password
from services.user_service.database import models
from services.user_service.database.database import SessionLocal


ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "Admin@12345"


def create_admin():
    db = SessionLocal()

    try:
        existing_user = db.query(models.User).filter(
            models.User.email == ADMIN_EMAIL
        ).first()

        if existing_user:
            if existing_user.role != "admin":
                existing_user.role = "admin"
                db.commit()
                print("Existing user promoted to admin.")
            else:
                print("Admin user already exists.")

            return

        admin = models.User(
            name="Admin",
            email=ADMIN_EMAIL,
            hashed_password=hash_password(ADMIN_PASSWORD),
            role="admin"
        )

        db.add(admin)
        db.commit()

        print("Admin user created successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()