from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class ChildBase(BaseModel):
    """Base child model with common fields"""
    first_name: str = Field(..., min_length=1, max_length=100, description="Child's first name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Child's last name")
    email: Optional[EmailStr] = Field(None, description="Child's email address")
    phone: Optional[str] = Field(None, max_length=20, description="Child's phone number")
    parent_id: str = Field(..., description="ID of the parent user")
    date_of_birth: Optional[str] = Field(None, description="Child's date of birth (YYYY-MM-DD)")
    grade: Optional[str] = Field(None, max_length=50, description="Child's current grade")
    school: Optional[str] = Field(None, max_length=255, description="Child's school name")
    emergency_contact: Optional[str] = Field(None, max_length=20, description="Emergency contact number")
    notes: Optional[str] = Field(None, description="Additional notes about the child")

class ChildCreate(ChildBase):
    """Model for creating a new child"""
    pass

class ChildUpdate(BaseModel):
    """Model for updating a child"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Child's first name")
    last_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Child's last name")
    email: Optional[EmailStr] = Field(None, description="Child's email address")
    phone: Optional[str] = Field(None, max_length=20, description="Child's phone number")
    parent_id: Optional[str] = Field(None, description="ID of the parent user")
    date_of_birth: Optional[str] = Field(None, description="Child's date of birth (YYYY-MM-DD)")
    grade: Optional[str] = Field(None, max_length=50, description="Child's current grade")
    school: Optional[str] = Field(None, max_length=255, description="Child's school name")
    emergency_contact: Optional[str] = Field(None, max_length=20, description="Emergency contact number")
    notes: Optional[str] = Field(None, description="Additional notes about the child")
    is_active: Optional[bool] = Field(None, description="Whether the child is active in the system")

class ChildResponse(ChildBase):
    """Model for child response"""
    id: str = Field(..., description="Unique child ID")
    is_active: bool = Field(..., description="Whether the child is active")
    created_at: datetime = Field(..., description="When the child was created")
    updated_at: datetime = Field(..., description="When the child was last updated")

    class Config:
        from_attributes = True 