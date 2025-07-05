from pydantic import BaseModel, Field
from typing import Optional

class UserLocationCreateRequest(BaseModel):
    user_id: str
    address: str
    latitude: float
    longitude: float
    lat: float
    lng: float
    accuracy: Optional[float] = None 