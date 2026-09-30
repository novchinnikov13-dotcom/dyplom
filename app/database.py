from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


# Production PostgreSQL
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://app_user:test123@localhost:5432/microblog"
)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"options": "-c client_encoding=UTF8"}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    """Dependency для FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
