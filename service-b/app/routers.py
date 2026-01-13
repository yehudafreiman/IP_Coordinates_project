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
    coordinates_data = load_external_data("http://localhost:8000/coordinates")
    validated_data = CoordinatesWithIP(**coordinates_data)
    redis_store(validated_data.ip, validated_data.dict())
    return {
        "message": "Coordinates saved successfully",
        "ip": validated_data.ip,
        "data": validated_data.dict()
    }

@router.get("/getCoordinates/{ip}", response_model=CoordinatesWithIP)
def get_coordinates(ip: str):
    data = redis_retrieve(ip)
    if data:
        return data
    raise HTTPException(status_code=404, detail="IP not found")