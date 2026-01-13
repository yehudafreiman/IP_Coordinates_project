from fastapi import APIRouter, HTTPException
from storage import redis_store, redis_retrieve, redis_conn
from schemas import CoordinatesWithIP

router = APIRouter()

# נקודת קצה לקבלת נתונים ושמירה ב-Redis
@router.post("/saveCoordinatesToRedis")
def save_coordinates_to_redis(data: CoordinatesWithIP):
    try:
        # קבל נתונים מ-Service A
        # בדוק שהנתונים תקינים
        # שמור ב-Redis
        redis_store(data.ip, data.model_dump())
        # החזר תשובה למשתמש
        return {
            "message": "Saved successfully",
            "ip": data.ip
        }
    # אם לא נתונים לא תקינים או שקיימת שגיאת חיבור – החזר שגיאה
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to save coordinates")

# שלוף נתונים מ-Redis לפי ה-IP
@router.get("/getCoordinates/{ip}", response_model=CoordinatesWithIP)
def get_coordinates(ip: str):
    data = redis_retrieve(ip)
    # אם נמצא ערך ב-Redis
    if data is not None:
        return data
    # אם לא נמצא ערך – החזר שגיאה
    raise HTTPException(status_code=404, detail="IP not found")

# שלוף את כל המפתחות מ-Redis
@router.get("/getAllCoordinates")
def get_all_coordinates():
    keys = redis_conn.keys("*")
    # אם אין מפתחות
    if not keys:
        return {"coordinates": []}
    # שלוף את כל הערכים
    all_data = []
    for key in keys:
        data = redis_retrieve(key)
        if data:
            all_data.append(data)
    # החזר את כל הנתונים
    return {"coordinates": all_data}
