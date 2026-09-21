from gateway.resilience.circuit_breaker import CircuitBreaker


# Create a circuit breaker using the configuration
# values from .env through config.py.
breaker = CircuitBreaker()


# --------------------------------
# Test: Open the circuit
# --------------------------------

# Simulate three consecutive failures.
for _ in range(3):
    breaker.record_failure()

print("State:", breaker.state)


# --------------------------------
# Test: HALF-OPEN recovery
# --------------------------------

# Skip the recovery timeout for testing
# instead of waiting 10 seconds.
breaker.opened_at -= breaker.recovery_timeout


# The first request should be allowed
# as the recovery probe.
print("First probe allowed:", breaker.allow_request())
print("State:", breaker.state)


# A second request should be blocked
# because the first recovery probe is still active.
print("Second probe allowed:", breaker.allow_request())
print("State:", breaker.state)


# --------------------------------
# Test: Successful recovery
# --------------------------------

# Simulate the recovery probe succeeding.
breaker.record_success()

print("After success:", breaker.state)
print("Probe in progress:", breaker.probe_in_progress)