from pydantic import BaseModel, Field, EmailStr
from typing import List

class CompanyCreateRequest(BaseModel):
    name: str
    description: str
    address: str
    phone: str
    email: EmailStr
    service_areas: List[str]
    city: str
    state: str
    zip_code: str
    country: str 