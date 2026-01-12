from redis import Redis

redis_conn = Redis(host="localhost", port=6379, decode_responses=True)

def redis_store(key, value):
    redis_conn.set(key, value)

def redis_retrieve(key):
    return redis_conn.get(key)

redis_store('foo', 'bar')
retrieved = redis_retrieve('foo')
print(retrieved)

redis_conn.close()
