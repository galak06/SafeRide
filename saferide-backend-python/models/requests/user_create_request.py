from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str
    last_name: str
    phone: Optional[str] = None
    role_id: str
    company_id: Optional[str] = None
    profile_picture: Optional[str] = None 