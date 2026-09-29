import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://microblog:microblog@localhost:5432/microblog",
)

MEDIA_ROOT = os.getenv("MEDIA_ROOT", "media")
