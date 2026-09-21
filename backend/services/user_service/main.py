from fastapi import FastAPI, Depends


from services.user_service.database import models
from services.user_service.schemas.user import UserResponse
from services.user_service.core.dependencies import get_current_user

from services.user_service.routes.auth import router as auth_router
from services.user_service.routes.users import router as users_router
from services.user_service.routes.admin import router as admin_router
from services.user_service.routes.health import router as health_router


app = FastAPI()

# Register authentication endpoints such as /auth/register and /auth/login.
app.include_router(auth_router)

# Register admin-only endpoints.
app.include_router(admin_router)


# User endpoints such as /users/me.
app.include_router(users_router)

#health check
app.include_router(health_router)

