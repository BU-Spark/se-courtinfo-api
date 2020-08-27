import redis

from app.core import config

rate_limit_redis_client = None
celery_redis_client = None


# Simple function to handle getting the current redis
# session
def get_redis_rate_limit_client() -> redis.Redis:
    global rate_limit_redis_client
    if not rate_limit_redis_client:
        rate_limit_redis_client = redis.from_url(config.REDIS_DB_URL)
    return rate_limit_redis_client

