from pydantic import BaseModel

class Coordinates(BaseModel):
    lat: int
    lon: int