from pydantic import BaseModel
from typing import Optional

class UserLocationUpdateRequest(BaseModel):
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_active: Optional[bool] = None 