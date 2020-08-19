import time

import redis
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Request, HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os
from app.redis_handler.redis_session import get_redis_client
import app.env_handler as envhandler

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv(envhandler.Hash_Key_Env_Key)
ALGORITHM = os.getenv(envhandler.Hash_Alg_Env_Key)
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv(envhandler.JWT_Token_TTL))


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def _over_limit(conn: redis.Redis, request: Request, duration: int, limit: int) -> bool:
    pipe = conn.pipeline(transaction=True)
    bucket = ':%i:%i' % (duration, time.time() // duration)
    ip = request.client.host
    key = ip + bucket
    pipe.incr(key)
    pipe.expire(key, duration)
    print('key:', key)
    if pipe.execute()[0] > limit:
        return True
    return False


# Heavily inspired by: https://www.binpress.com/rate-limiting-with-redis-1/
# Takes a redis connection and a request and an optional limit, checks against the redis cache
# to see if this user is rate limited
def _over_limit_multi(conn: redis.Redis, request: Request, limits=None):
    if limits is None:
        limits = [(1, 10), (60, 120), (3600, 240)]
    for duration, limit in limits:
        if _over_limit(conn, request, duration, limit):
            return True
    return False


# Raise an exception if the user(ip) has exceeded the rate limit
def user_over_rate_limit(request: Request) -> None:
    r_client = get_redis_client()
    if _over_limit_multi(r_client, request):
        raise HTTPException(status_code=429, detail="request exceeded limit")
    return None
