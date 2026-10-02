import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://app_user:test123@localhost:5432/microblog",
)

MEDIA_ROOT = os.getenv("MEDIA_ROOT", "media")
