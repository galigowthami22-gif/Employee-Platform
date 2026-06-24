import redis
from core.config import settings

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)

def set_value(key, value, expiry=300):
    redis_client.set( key, value, ex=expiry)

def get_value(key):
    return redis_client.get(key)

def delete_value(key):
    redis_client.delete(key)