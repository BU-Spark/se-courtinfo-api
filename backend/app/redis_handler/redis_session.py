import redis

redis_client = None


# Simple function to handle getting the current redis
# session
def get_redis_client() -> redis.Redis:
    global redis_client
    if not redis_client:
        redis_client = redis.Redis(
            host='redis',
            port='6379',
            db='1'
        )
    return redis_client
