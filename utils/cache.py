import json
from utils.redis_manager import redis_client

def get_cache(key):
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    return None

def set_cache(key, value, expiry=300):
    redis_client.set(key, json.dumps(value), ex=expiry)