from gateway.resilience.circuit_manager import circuit_manager


# Get the breaker for User Service.
users_breaker = circuit_manager.get_breaker("users")

# Get the breaker for Order Service.
orders_breaker = circuit_manager.get_breaker("orders")


# Simulate User Service failures.
for _ in range(3):
    users_breaker.record_failure()


print("Users breaker:", users_breaker.state)
print("Orders breaker:", orders_breaker.state)


# Check whether the User Service circuit is open.
print("Users request allowed:", users_breaker.allow_request())

# Check whether the Order Service circuit is still available.
print("Orders request allowed:", orders_breaker.allow_request())