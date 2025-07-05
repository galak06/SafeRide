from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class CompanyUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    service_areas: Optional[List[str]] = None
    is_active: Optional[bool] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None 