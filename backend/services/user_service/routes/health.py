from fastapi import APIRouter
from sqlalchemy import text

from services.user_service.database.database import engine


router = APIRouter(
    tags=["Health"]
)


@router.get("/health")
def health_check():
    try:
        # Run a simple database query to confirm
        # that the database connection is working.
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "service": "user-service",
            "database": "healthy"
        }

    except Exception:
        return {
            "status": "unhealthy",
            "service": "user-service",
            "database": "unhealthy"
        }