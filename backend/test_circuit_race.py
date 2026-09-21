import asyncio

from gateway.resilience.circuit_breaker import CircuitBreaker


async def test_half_open_probe():
    breaker = CircuitBreaker(
        failure_threshold=3,
        recovery_timeout=0
    )

    # Force the breaker into OPEN state.
    for _ in range(3):
        breaker.record_failure()

    # recovery_timeout=0 means it can immediately become HALF-OPEN.
    results = await asyncio.gather(
        *[breaker.allow_request() for _ in range(10)]
    )

    print("Results:", results)
    print("Allowed probes:", results.count(True))
    print("Blocked requests:", results.count(False))


asyncio.run(test_half_open_probe())