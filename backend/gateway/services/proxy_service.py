import httpx
from fastapi import HTTPException, Request

from gateway.resilience.circuit_manager import circuit_manager
from gateway.resilience.retry import retry_request


async def forward_request(
    request: Request,
    service_name: str,
    service_url: str,
    upstream_path: str
):
    url = f"{service_url}{upstream_path}"

    breaker = circuit_manager.get_breaker(service_name)

    if not await breaker.allow_request():
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")

    content = await request.body()

    # Only forward headers the client actually sent —
  
    headers = {}

    content_type = request.headers.get("content-type")
    authorization = request.headers.get("authorization")

    if content_type:
        headers["content-type"] = content_type

    if authorization:
        headers["authorization"] = authorization

    async with httpx.AsyncClient() as client:
        try:
            response = await retry_request(
                client=client,
                method=request.method,
                url=url,
                content=content,
                headers=headers,
                params=request.query_params
            )

            if 500 <= response.status_code < 600:
                breaker.record_failure()
                raise HTTPException(status_code=response.status_code, detail="Upstream service error")

            breaker.record_success()
            return response

        except httpx.ConnectError:
            breaker.record_failure()
            raise HTTPException(status_code=503, detail="Service unavailable")

        except httpx.TimeoutException:
            breaker.record_failure()
            raise HTTPException(status_code=504, detail="Upstream service timed out")

        except httpx.HTTPError:
            raise HTTPException(status_code=502, detail="Error communicating with upstream service")