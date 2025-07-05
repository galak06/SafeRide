from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

class UserModel(BaseModel):
    id: str = Field(..., description="User ID")
    email: EmailStr = Field(..., description="User email")
    password_hash: str = Field(..., description="Hashed password")
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    phone: Optional[str] = Field(None, description="Phone number")
    role_id: str = Field(..., description="Role ID")
    company_id: Optional[str] = Field(None, description="Company ID if user belongs to a company")
    is_active: bool = Field(True, description="Whether user is active")
    is_verified: bool = Field(False, description="Whether email is verified")
    profile_picture: Optional[str] = Field(None, description="Profile picture URL")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    # Relationship fields
    parent_ids: List[str] = Field(default_factory=list, description="List of parent user IDs")
    child_ids: List[str] = Field(default_factory=list, description="List of child user IDs")
    escort_ids: List[str] = Field(default_factory=list, description="List of escort user IDs")
    is_child: bool = Field(False, description="Whether user is a child")
    is_parent: bool = Field(False, description="Whether user is a parent")
    is_escort: bool = Field(False, description="Whether user is an escort") 