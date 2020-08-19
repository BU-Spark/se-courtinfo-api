import redis

rate_limit_redis_client = None
celery_redis_client = None


# Simple function to handle getting the current redis
# session
def get_redis_rate_limit_client() -> redis.Redis:
    global rate_limit_redis_client
    if not rate_limit_redis_client:
        rate_limit_redis_client = redis.Redis(
            host='redis',
            port='6379',
            db='2'
        )
    return rate_limit_redis_client


def get_celery_redis_client() -> redis.Redis:
    global celery_redis_client
    if not celery_redis_client:
        celery_redis_client = redis.Redis(
            host='redis',
            port='6379',
            db='1'
        )
    return celery_redis_client
