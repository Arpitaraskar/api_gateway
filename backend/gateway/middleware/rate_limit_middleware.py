import time
import redis

from pathlib import Path

from fastapi import Request
from fastapi.responses import JSONResponse

from gateway.core.redis import redis_client
from gateway.core.config import BUCKET_CAPACITY, REFILL_RATE


SCRIPT_PATH = (
    Path(__file__).parent.parent
    / "scripts"
    / "token_bucket.lua"
)

with open(SCRIPT_PATH, "r") as file:
    TOKEN_BUCKET_SCRIPT = file.read()


async def rate_limit(request: Request, call_next):

    client_ip = request.client.host

    redis_key = f"token_bucket:{client_ip}"

    try:
        
#Problem: Concurrent requests → race condition
#Solution: Atomic Lua execution in Redis

# Run the entire token bucket operation atomically in Redis.
# This prevents race conditions where concurrent requests could
# read the same token count and both incorrectly consume a token.

        result = redis_client.eval(
            TOKEN_BUCKET_SCRIPT,
            1,
            redis_key,
            BUCKET_CAPACITY,
            REFILL_RATE,
            time.time()
        )

        allowed = result[0]
        tokens_remaining = result[1]
        retry_after = result[2]

        if allowed == 0:

            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded",
                    "retry_after": retry_after
                },
                headers={
                    "X-RateLimit-Limit": str(BUCKET_CAPACITY),
                    "X-RateLimit-Remaining": "0",
                    "Retry-After": str(retry_after)
                }
            )

    except redis.exceptions.ConnectionError:
        # Fail open: Redis is unavailable,
        # so allow the request instead of crashing.
        return await call_next(request)

    response = await call_next(request)

    response.headers["X-RateLimit-Limit"] = str(BUCKET_CAPACITY)

    response.headers["X-RateLimit-Remaining"] = str(
        int(tokens_remaining)
    )

    return response