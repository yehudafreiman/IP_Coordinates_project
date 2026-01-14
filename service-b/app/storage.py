from redis import Redis
import json
import os

# חיבור ל-Redis באמצעות משתני סביבה
redis_conn = Redis(
    host=os.getenv("REDIS_HOST", "redis-headless"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True
)

# שמירת נתונים במסד נתונים
def redis_store(key, value):
    # אם ה- value שהתקבל הוא dictionary
    if isinstance(value, dict):
        # המר לפורמט json
        value = json.dumps(value)
    # אחסן במסד נתונים
    redis_conn.set(key, value)

# שליפת נתונים ממסד נתונים
def redis_retrieve(key):
    # שלוף נתונים ממסד נתונים
    value = redis_conn.get(key)
    # אם לא התקבלו נתונים
    if value is None:
        return None
    try:
        # המר לפורמט json
        return json.loads(value)
    # אם ההמרה נכשלה החזר כמו שזה
    except json.JSONDecodeError:
        return value
