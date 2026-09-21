import asyncio
import time

from gateway.core.config import (
    CIRCUIT_FAILURE_THRESHOLD,
    CIRCUIT_RECOVERY_TIMEOUT
)


class CircuitBreaker:

    def __init__(
        self,
        failure_threshold: int = CIRCUIT_FAILURE_THRESHOLD,
        recovery_timeout: int = CIRCUIT_RECOVERY_TIMEOUT
    ):
        # Number of failures required before opening the circuit.
        self.failure_threshold = failure_threshold

        # Time to wait before allowing a recovery test.
        self.recovery_timeout = recovery_timeout

        # Circuit starts in normal operation.
        self.state = "CLOSED"

        # Number of consecutive upstream failures.
        self.failure_count = 0

        # Time when the circuit was opened.
        self.opened_at = None

        # Tracks whether a HALF-OPEN recovery probe is already running.
        self.probe_in_progress = False

        # Protects the check + update of probe_in_progress.
        #
        # Without this lock, two concurrent requests could both check
        # probe_in_progress == False before either one sets it to True.
        #
        # That would allow multiple recovery probes at the same time.
        self.probe_lock = asyncio.Lock()

    def record_failure(self):

        # Increase the failure count.
        self.failure_count += 1

        # If the HALF-OPEN recovery test failed,
        # the service is still unhealthy.
        if self.state == "HALF-OPEN":
            self.state = "OPEN"
            self.opened_at = time.time()
            self.probe_in_progress = False

            return

        # Open the circuit after reaching the failure threshold.
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            self.opened_at = time.time()

    def record_success(self):

        # Successful request means the service is healthy.
        self.failure_count = 0
        self.state = "CLOSED"
        self.opened_at = None

        # Recovery probe has finished.
        self.probe_in_progress = False

    async def allow_request(self):

        # CLOSED means requests are allowed.
        if self.state == "CLOSED":
            return True

        # OPEN means we need to check recovery time.
        if self.state == "OPEN":

            elapsed_time = time.time() - self.opened_at

            # Recovery time has passed.
            if elapsed_time >= self.recovery_timeout:
                self.state = "HALF-OPEN"

            else:
                return False

        # HALF-OPEN allows only one recovery probe.
        if self.state == "HALF-OPEN":

            # Protect the check + update as one operation.
            #
            # Only one concurrent request can enter this section
            # at a time.
            async with self.probe_lock:

                # Another request is already performing
                # the recovery probe.
                if self.probe_in_progress:
                    return False

                # This request becomes the single recovery probe.
                self.probe_in_progress = True

                return True

        return False