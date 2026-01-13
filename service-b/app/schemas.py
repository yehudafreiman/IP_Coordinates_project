from pydantic import BaseModel, Field

class Coordinates(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lon: float = Field(..., ge=-180, le=180, description="Longitude")

class CoordinatesWithIP(Coordinates):
    ip: str