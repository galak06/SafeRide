from pydantic import BaseModel, Field
from typing import List
from .parent_child_relationship_response import ParentChildRelationshipResponse

class UserRelationshipsResponse(BaseModel):
    user_id: str = Field(..., description="User ID")
    relationships: List[ParentChildRelationshipResponse] = Field(..., description="List of relationships")
    
    class Config:
        from_attributes = True 