from redis import Redis
import json

redis_conn = Redis(host="localhost", port=6379, decode_responses=True)

def redis_store(key, value):
    if isinstance(value, dict):
        value = json.dumps(value)
    redis_conn.set(key, value)

def redis_retrieve(key):
    value = redis_conn.get(key)
    if value:
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return None