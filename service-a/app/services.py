from fastapi import HTTPException
import requests

def get_coordinates_data(url):
    try:
        response = requests.get(url)
        info = response.json()
    except Exception:
        raise HTTPException(status_code=502, detail="External API error")
    if info["status"] != "success":
        raise HTTPException(status_code=400, detail="Invalid IP")

    data = {"ip": info["query"], "lat": info["lat"], "lon": info["lon"]}
    return data