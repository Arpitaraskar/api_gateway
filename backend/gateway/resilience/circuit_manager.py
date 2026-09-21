from gateway.resilience.circuit_breaker import CircuitBreaker


class CircuitBreakerManager:
    """
    Keeps one CircuitBreaker instance for each upstream service.

    Why:
    A failure in User Service should not open the circuit
    for other services such as Order Service or Payment Service.
    """

    def __init__(self):
        # Each service gets its own persistent CircuitBreaker object.
        self.breakers = {}

    def get_breaker(self, service_name: str) -> CircuitBreaker:
        """
        Return the CircuitBreaker belonging to the given service.

        If the service does not have a breaker yet, create one.
        """

        if service_name not in self.breakers:
            self.breakers[service_name] = CircuitBreaker()

        return self.breakers[service_name]


# One manager instance is shared by the Gateway process.
circuit_manager = CircuitBreakerManager()