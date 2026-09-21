from fastapi import Request

from gateway.core.logger import logger


async def log_requests(request: Request, call_next):

    request_id = request.state.request_id

    logger.info(
        f"[{request_id}] Incoming request: "
        f"{request.method} {request.url.path}"
    )

    try:
        response = await call_next(request)

        logger.info(
            f"[{request_id}] Response status: "
            f"{response.status_code}"
        )

        return response

    except Exception:

        logger.exception(
            f"[{request_id}] Request failed"
        )

        raise