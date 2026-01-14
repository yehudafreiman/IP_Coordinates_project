from fastapi import APIRouter, Body
from pydantic import IPvAnyAddress
from services import *

router = APIRouter()

@router.post("/")
def locate_ip(ip_address: IPvAnyAddress =Body(...)):
    url = f"http://ip-api.com/json/{ip_address}"
    data = get_coordinates_data(url)
    url = "http://storage_api:8001/saveCoordinatesToRedis"
    info = send_to_service_b(url, data)
    return info