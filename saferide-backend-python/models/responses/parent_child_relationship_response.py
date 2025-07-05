from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ParentChildRelationshipResponse(BaseModel):
    id: str = Field(..., description="Relationship ID")
    parent_id: str = Field(..., description="Parent user ID")
    child_id: str = Field(..., description="Child user ID")
    escort_id: Optional[str] = Field(None, description="Escort user ID")
    relationship_type: str = Field(..., description="Type of relationship")
    is_active: bool = Field(True, description="Whether the relationship is active")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        from_attributes = True 