import asyncio
import httpx

from gateway.core.config import (
    MAX_RETRIES,
    RETRY_BACKOFF_BASE,
    UPSTREAM_TIMEOUT
)


async def retry_request(
    client: httpx.AsyncClient,
    method: str,
    url: str,
    content: bytes,
    headers: dict,
    params=None
):
    # Retry GET requests only.
    if method != "GET":
        return await client.request(
            method=method,
            url=url,
            content=content,
            headers=headers,
            params=params,
            timeout=UPSTREAM_TIMEOUT
        )

    # Try the original request plus retries.
    for attempt in range(MAX_RETRIES + 1):

        try:
            return await client.request(
                method=method,
                url=url,
                content=content,
                headers=headers,
                params=params,
                timeout=UPSTREAM_TIMEOUT
            )

        except (httpx.ConnectError, httpx.TimeoutException):

            if attempt == MAX_RETRIES:
                raise

            # Wait before trying again.
            delay = RETRY_BACKOFF_BASE ** attempt

            await asyncio.sleep(delay)