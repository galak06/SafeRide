from pydantic import BaseModel, Field, EmailStr
from typing import List
from datetime import datetime

class DriverCompany(BaseModel):
    id: str = Field(..., description="Company ID")
    name: str = Field(..., description="Company name")
    description: str = Field(..., description="Company description")
    address: str = Field(..., description="Company address")
    phone: str = Field(..., description="Company phone")
    email: EmailStr = Field(..., description="Company email")
    service_areas: List[str] = Field(..., description="List of service area IDs")
    drivers: List[str] = Field(..., description="List of driver user IDs")
    is_active: bool = Field(True, description="Whether company is active")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

# Alias for DriverCompany to match service imports
CompanyModel = DriverCompany 