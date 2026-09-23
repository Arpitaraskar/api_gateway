from fastapi import APIRouter, Depends



from services.user_service.core.dependencies import get_current_user
from services.user_service.database import models
from services.user_service.schemas.user import UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: models.User = Depends(get_current_user)
):
   
    #  loads the authenticated user from the database.
    return current_user


# @router.get("/slow")
# async def slow_endpoint():
#     # Temporary endpoint used to verify that the Gateway
#     # stops waiting when an upstream service takes too long.
#     await asyncio.sleep(10)

#     return {
#         "message": "Slow response completed"
#     }

@router.get("/test")
def test_query(limit: int):
    return {
        "limit": limit
    }

@router.get("/{user_id}")
def get_user(user_id: int):
    return {
        "id": user_id,
        "name": f"User {user_id}"
    }

#request body forwarding