import os
from dotenv import load_dotenv
import hashlib



APP_ENV = os.getenv("APP_ENV", "development")

load_dotenv(".env")

if APP_ENV == "test":
    load_dotenv(".env.test", override=True)



secret = os.getenv("JWT_SECRET")

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")

RATE_LIMIT=int(os.getenv("RATE_LIMIT",10))
RATE_LIMIT_WINDOW=int(os.getenv("RATE_LIMIT_WINDOW",60))

BUCKET_CAPACITY=int(os.getenv("BUCKET_CAPACITY",10))
REFILL_RATE=int(os.getenv("REFILL_RATE", 1))


JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_MINUTES = int(
    os.getenv("JWT_EXPIRATION_MINUTES", 30)
)


MAX_RETRIES = int(os.getenv("MAX_RETRIES", 2))
RETRY_BACKOFF_BASE = int(os.getenv("RETRY_BACKOFF_BASE", 2))

UPSTREAM_TIMEOUT=int(os.getenv("UPSTREAM_TIMEOUT",5))

CIRCUIT_FAILURE_THRESHOLD=int(os.getenv("CIRCUIT_FAILURE_THRESHOLD",3))
CIRCUIT_RECOVERY_TIMEOUT=int(os.getenv("CIRCUIT_RECOVERY_TIMEOUT",10))



REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))