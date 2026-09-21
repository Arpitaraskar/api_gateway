

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from fastapi import Depends

from gateway.routing.routes import get_route
from gateway.services.proxy_service import forward_request
from gateway.middleware.logging_middleware import log_requests
from gateway.middleware.request_id_middleware import add_request_id
from gateway.core.redis import redis_client
from gateway.middleware.rate_limit_middleware import rate_limit
from gateway.routing.health import router as health_router
from gateway.core.auth import get_current_user


app = FastAPI()

app.middleware("http")(rate_limit)
app.middleware("http")(log_requests)
app.middleware("http")(add_request_id)
app.include_router(health_router)

async def handle_gateway_request(
    service_name: str,
    request: Request,
    path: str = ""
):
    route = get_route(service_name)

    if route is None:
        raise HTTPException(
            status_code=404,
            detail="Service route not found"
        )

    upstream_path = route["upstream_path"]

    if path:
        upstream_path = f"{upstream_path}/{path}"

    response = await forward_request(
    request=request,
    service_name=service_name,
    service_url=route["service_url"],
    upstream_path=upstream_path
)
    return Response(
    content=response.content,
    status_code=response.status_code,
    headers=dict(response.headers),
    media_type=response.headers.get("content-type")
)

@app.get("/api/{service_name}")
async def gateway_root_get(
    service_name: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    return await handle_gateway_request(
        service_name=service_name,
        request=request
    )


@app.post("/api/{service_name}")
async def gateway_root_post(
    service_name: str,
    request: Request
    
):
    return await handle_gateway_request(
        service_name=service_name,
        request=request
    )


@app.get("/api/{service_name}/{path:path}")
async def gateway_path_get(
    service_name: str,
    path: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    return await handle_gateway_request(
        service_name=service_name,
        request=request,
        path=path
    )


@app.post("/api/{service_name}/{path:path}")
async def gateway_path_post(
    service_name: str,
    path: str,
    request: Request
    
):
    return await handle_gateway_request(
        service_name=service_name,
        request=request,
        path=path
    )
