import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


# Load environment variables from the .env file.
load_dotenv()


# Read the database connection string from the environment.
# This keeps database configuration outside the source code and
# allows different databases to be used in development and deployment.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./user_service.db"
)


# SQLite needs this option because FastAPI can handle requests
# using different threads.
connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False
    }


engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


class Base(DeclarativeBase):
    pass


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()