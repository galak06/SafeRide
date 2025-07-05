from pydantic import BaseModel, Field
from typing import Optional

class UserUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    role_id: Optional[str] = None
    company_id: Optional[str] = None
    is_active: Optional[bool] = None
    profile_picture: Optional[str] = None 