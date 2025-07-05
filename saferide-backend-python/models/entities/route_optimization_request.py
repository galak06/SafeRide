from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class RouteOptimizationRequest(BaseModel):
    company_id: str = Field(..., description="Company ID")
    driver_id: str = Field(..., description="Driver ID")
    user_locations: List[str] = Field(..., description="List of user location IDs to include")
    optimization_type: str = Field("shortest_distance", description="Optimization type: shortest_distance, fastest_route, balanced")
    max_stops: Optional[int] = Field(None, description="Maximum number of stops")
    time_window_start: Optional[datetime] = Field(None, description="Start of time window")
    time_window_end: Optional[datetime] = Field(None, description="End of time window") 