import redis
from core.config import settings

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)

def set_cache(key, value, expire=300):
    redis_client.set(key, value, ex=expire)

def get_cache(key):
    return redis_client.get(key)

def delete_cache(key):
    redis_client.delete(key)