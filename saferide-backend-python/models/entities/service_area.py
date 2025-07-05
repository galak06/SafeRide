from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime

class ServiceArea(BaseModel):
    id: str = Field(..., description="Service area ID")
    name: str = Field(..., description="Service area name")
    description: str = Field(..., description="Service area description")
    coordinates: List[Dict[str, float]] = Field(..., description="Polygon coordinates defining the service area")
    is_active: bool = Field(True, description="Whether service area is active")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

# Alias for ServiceArea to match service imports
ServiceAreaModel = ServiceArea 