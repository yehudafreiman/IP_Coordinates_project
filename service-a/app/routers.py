from fastapi import APIRouter, Body
from pydantic import IPvAnyAddress
from services import *

router = APIRouter()

@router.post("/")
def locate_ip(ip_address: IPvAnyAddress =Body(...)):
    url = f"http://ip-api.com/json/{ip_address}"
    data = get_coordinates_data(url)
    return data
