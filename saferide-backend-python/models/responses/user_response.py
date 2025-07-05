from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from ..base.role_model import RoleModel
from ..entities.driver_company import DriverCompany

class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str]
    role: RoleModel
    company: Optional[DriverCompany]
    is_active: bool
    is_verified: bool
    profile_picture: Optional[str]
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] 