from fastapi import APIRouter, HTTPException
import requests
from storage import redis_store, redis_retrieve
from schemas import CoordinatesWithIP

# פונקציית עזר
def load_external_data(url):
    # שלוף נתונים מ-url
    response = requests.get(url)
    # החזר בפורמט json
    return response.json()

router = APIRouter()

# נקודת קצה לקבלת נתונים ושמירה במסד נתונים
@router.post("/saveCoordinatesToRedis")
def save_coordinates_to_redis():
    try:
        # שלוף נתונים מ-Service A
        data = load_external_data("http://localhost:8000/coordinates")
        # בדוק שהנתונים תקינים
        validated = CoordinatesWithIP(**data)
        # שמור ב-Redis
        redis_store(validated.ip, validated.model_dump())
        # החזר תשובה למשתמש
        return {
            "message": "Saved successfully",
            "ip": validated.ip
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