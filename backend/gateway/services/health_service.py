import httpx

from gateway.core.config import UPSTREAM_TIMEOUT


async def check_service_health(service_url: str) -> dict:
    """
    Get the health information from an upstream service.

    Returns the service's health response as a dictionary.
    """

    health_url = f"{service_url}/health"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                health_url,
                timeout=UPSTREAM_TIMEOUT
            )

        if response.status_code == 200:
            return response.json()

        return {
            "status": "unhealthy"
        }

    except httpx.HTTPError:
        return {
            "status": "unhealthy"
        }