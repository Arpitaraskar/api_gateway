#core/config.py
import os 
import hashlib

from dotenv import load_dotenv

load_dotenv()

#temporary for checking
print("USER SERVICE JWT SECRET LOADED:", bool(os.getenv("JWT_SECRET")))
print("USER SERVICE JWT ALGORITHM:", os.getenv("JWT_ALGORITHM"))

secret = os.getenv("JWT_SECRET")

JWT_SECRET= os.getenv("JWT_SECRET")

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

JWT_EXPIRATION_MINUTES = int(
    os.getenv("JWT_EXPIRATION_MINUTES",30)
)

if not JWT_SECRET:
    raise RuntimeError(
        "JWT_SECRET environment variable is required"
    )


print(
    "JWT SECRET FINGERPRINT:",
    hashlib.sha256(secret.encode()).hexdigest()[:12]
)