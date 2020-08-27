import os
from typing import Final

PROJECT_NAME: Final[str] = "Suffolk County District Attorney API"
# Full Database URL, includes host, user, password, port and database name
SQLALCHEMY_DATABASE_URI: Final[str] = os.getenv("DATABASE_URL")
API_V1_STR: Final[str] = "/api/v1"
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
# Postgres DB Host
POSTGRES_DB_URL_PORT: Final[str] = os.getenv("POSTGRES_URL_PORT")
# Postgres DB Name
POSTGRES_DB_NAME: Final[str] = os.getenv("POSTGRES_DB_NAME")
# AWS S3 Pre-signed URL Expiration Times in seconds
S3_LINK_TTL: Final[int] = 120
# Full Redis URL
REDIS_DB_URL: Final[str] = os.getenv("REDIS_DB_URL")
