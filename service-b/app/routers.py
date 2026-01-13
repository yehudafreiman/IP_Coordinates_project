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
    # שלוף נתונים מ-Service A
    data = load_external_data("http://localhost:8000/coordinates")
    # בדוק שהנתונים תקינים
    validated = CoordinatesWithIP(**data)
    # שמור ב-Redis
    redis_store(validated.ip, validated.dict())
    # החזר תשובה למשתמש
    return {"message": "Saved successfully", "ip": validated.ip}

# נקודת קצה לקבלת נתונים ממסד נתונים והחזרה למשתמש
@router.get("/getCoordinates/{ip}", response_model=CoordinatesWithIP)
def get_coordinates(ip: str):
    # שלוף נתונים ממסד נתונים
    data = redis_retrieve(ip)
    # אם התקבלו נתונים החזר אותם למשתמש
    if data:
        return data
    # אם לא התקבלו נתונים החזר שגיאה
    raise HTTPException(status_code=404, detail="IP not found")