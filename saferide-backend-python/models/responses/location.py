from pydantic import BaseModel, Field
from typing import Optional

class Location(BaseModel):
    lat: float = Field(..., description="Latitude")
    lng: float = Field(..., description="Longitude")
    address: Optional[str] = Field(None, description="Human-readable address") 