from fastapi import APIRouter, HTTPException
import requests
from schemas import IPValidation

router = APIRouter()

@router.post("/")
def locate_ip(ip_address: IPValidation):
    url = f"http://ip-api.com/json/{ip_address.ip}"
    
    try:
        res = requests.get(url)
        info = res.json()
    except Exception:
        raise HTTPException(status_code=502, detail="External API error")

    if info.get("status") != "success":
        raise HTTPException(status_code=400, detail="Invalid IP")

    data = {
        "ip": info["query"],
        "Coordinates": {
                    "lat": info["lat"],
                    "lon": info["lon"]
        }
    }
    return data