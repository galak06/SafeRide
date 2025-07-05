from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime

class RoutePlan(BaseModel):
    id: str = Field(..., description="Route plan ID")
    company_id: str = Field(..., description="Company ID")
    driver_id: str = Field(..., description="Driver ID")
    name: str = Field(..., description="Route plan name")
    description: str = Field(..., description="Route plan description")
    stops: List[Dict[str, Any]] = Field(..., description="List of stops with user info and order")
    total_distance: float = Field(..., description="Total route distance in km")
    estimated_duration: int = Field(..., description="Estimated duration in minutes")
    is_active: bool = Field(True, description="Whether route plan is active")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now) 