from pydantic import BaseModel, Field
from typing import Optional
from ..responses.location import Location

class RideRequest(BaseModel):
    user_id: str = Field(..., description="User ID requesting the ride")
    origin: Location = Field(..., description="Pickup location")
    destination: Location = Field(..., description="Drop-off location")
    passenger_count: int = Field(1, ge=1, le=4, description="Number of passengers")
    notes: Optional[str] = Field(None, description="Additional ride notes") 