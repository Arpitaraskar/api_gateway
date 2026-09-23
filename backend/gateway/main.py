from fastapi import FastAPI

from gateway.middleware.logging_middleware import log_requests
from gateway.middleware.rate_limit_middleware import rate_limit
from gateway.middleware.request_id_middleware import add_request_id
from gateway.routing.gateway import router as gateway_router
from gateway.routing.health import router as health_router


app = FastAPI()

app.middleware("http")(rate_limit)
app.middleware("http")(log_requests)
app.middleware("http")(add_request_id)

app.include_router(gateway_router)
app.include_router(health_router)