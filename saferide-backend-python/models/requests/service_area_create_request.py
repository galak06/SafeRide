from pydantic import BaseModel, Field
from typing import List, Dict

class ServiceAreaCreateRequest(BaseModel):
    company_id: str
    name: str
    description: str
    coordinates: List[Dict[str, float]]
    center_lat: float
    center_lng: float
    radius_km: float 