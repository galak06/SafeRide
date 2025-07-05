from pydantic import BaseModel, Field
from typing import Optional

class ParentChildRelationshipCreate(BaseModel):
    parent_id: str = Field(..., description="Parent user ID")
    child_id: str = Field(..., description="Child user ID")
    escort_id: Optional[str] = Field(None, description="Escort user ID")
    relationship_type: str = Field(..., description="Type of relationship")

class ParentChildRelationshipUpdate(BaseModel):
    escort_id: Optional[str] = Field(None, description="Escort user ID")
    relationship_type: Optional[str] = Field(None, description="Type of relationship")
    is_active: Optional[bool] = Field(None, description="Whether the relationship is active") 