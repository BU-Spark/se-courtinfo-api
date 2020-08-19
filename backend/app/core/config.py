import os
from typing import Final

PROJECT_NAME = "Suffolk County District Attorney API"
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
API_V1_STR = "/api/v1"
# AWS S3 Access ID used for internal API operations
S3_KEY_INTERNAL: Final[str] = os.getenv("S3_KEY_INTERNAL")
# AWS S3 Secret for internal API operations
S3_SECRET_INTERNAL: Final[str] = os.getenv("S3_SECRET_INTERNAL")
# AWS S3 Bucket Name
S3_BUCKET_NAME: Final[str] = os.getenv("S3_BUCKET_NAME")
# Postgres Username
POSTGRES_USER_NAME: Final[str] = os.getenv("POSTGRES_USER")
# Postgres Password
POSTGRES_PASSWORD: Final[str] = os.getenv("POSTGRES_PASSWORD")