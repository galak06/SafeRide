from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class RideResponse(BaseModel):
    ride_id: str = Field(..., description="Unique ride identifier")
    status: str = Field(..., description="Current ride status")
    driver_info: Optional[Dict[str, Any]] = Field(None, description="Driver information if assigned")
    estimated_pickup: datetime = Field(..., description="Estimated pickup time")
    estimated_arrival: datetime = Field(..., description="Estimated arrival time")
    fare_estimate: float = Field(..., description="Estimated fare amount") 