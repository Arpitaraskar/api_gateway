#core/config.py
import os 
import hashlib

from dotenv import load_dotenv

load_dotenv()



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


