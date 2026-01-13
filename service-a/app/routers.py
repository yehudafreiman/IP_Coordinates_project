from fastapi import APIRouter, Body, HTTPException
from pydantic import IPvAnyAddress
import requests, json
from schemas import IPValidation

router = APIRouter()

@router.post("/")
def locate_ip(ip_address: IPvAnyAddress =Body(...)):
    url = f"http://ip-api.com/json/{ip_address}"
    
    try:
        response = requests.get(url)
        info = response.json()
    except Exception:
        raise HTTPException(status_code=502, detail="External API error")
    if info["status"] != "success":
        raise HTTPException(status_code=400, detail="Invalid IP")

    data = {"ip": info["query"], "lat": info["lat"], "lon": info["lon"]}
    return data