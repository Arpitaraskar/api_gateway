from fastapi import APIRouter

from gateway.routing.routes import get_route
from gateway.services.health_service import check_service_health


router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("/{service_name}")
async def service_health(service_name: str):
    """
    Check the health of an upstream service.
    """

    route = get_route(service_name)

    if route is None:
        return {
            "status": "unknown",
            "service": service_name
        }

    health_data = await check_service_health(
        route["service_url"]
    )

    return health_data