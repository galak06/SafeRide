from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class RoleModel(BaseModel):
    id: str = Field(..., description="Role ID")
    name: str = Field(..., description="Role name")
    description: str = Field(..., description="Role description")
    permissions: List[str] = Field(..., description="List of permission IDs")
    is_active: bool = Field(True, description="Whether role is active")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now) 