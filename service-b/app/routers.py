from fastapi import APIRouter, HTTPException
import requests
from storage import redis_store, redis_retrieve
from schemas import CoordinatesWithIP

def load_external_data(url):
    response = requests.get(url)
    return response.json()

router = APIRouter()

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

@router.get("/getCoordinates/{ip}", response_model=CoordinatesWithIP)
def get_coordinates(ip: str):
    data = redis_retrieve(ip)
    if data:
        return data
    raise HTTPException(status_code=404, detail="IP not found")