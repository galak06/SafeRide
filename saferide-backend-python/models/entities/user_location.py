from pydantic import BaseModel, Field
from datetime import datetime

class UserLocation(BaseModel):
    id: str = Field(..., description="Location ID")
    user_id: str = Field(..., description="User ID")
    address: str = Field(..., description="User address")
    latitude: float = Field(..., description="Latitude")
    longitude: float = Field(..., description="Longitude")
    is_active: bool = Field(True, description="Whether location is active")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now) 