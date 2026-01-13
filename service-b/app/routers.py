from fastapi import APIRouter, HTTPException
from storage import redis_store, redis_retrieve
from schemas import CoordinatesWithIP

router = APIRouter()

# נקודת קצה לקבלת נתונים ושמירה במסד נתונים
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

# נקודת קצה לקבלת נתונים ממסד נתונים והחזרה למשתמש
@router.get("/getCoordinates/{ip}", response_model=CoordinatesWithIP)
def get_coordinates(ip: str):
    # שלוף נתונים ממסד נתונים לפי ה-IP
    data = redis_retrieve(ip)
    # אם נמצא ערך ב-Redis
    if data is not None:
        return data
    # אם לא נמצא ערך – החזר שגיאה
    raise HTTPException(status_code=404, detail="IP not found")
