import json
import redis
from app.config.settings import settings

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def set_cache(key: str, value, expiration: int = 3600):
    redis_client.set(key, json.dumps(value), ex=expiration)


def get_cache(key: str):
    value = redis_client.get(key)
    if value:
        return json.loads(value)

    return None


def delete_cache(key: str):
    redis_client.delete(key)


def cache_exists(key: str):
    return redis_client.exists(key)
