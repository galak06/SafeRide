from pydantic import BaseModel
from typing import List, Dict, Optional

class ServiceAreaUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    coordinates: Optional[List[Dict[str, float]]] = None
    is_active: Optional[bool] = None 