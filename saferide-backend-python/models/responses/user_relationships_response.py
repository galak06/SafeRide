from pydantic import BaseModel, Field
from typing import List
from .parent_child_relationship_response import ParentChildRelationshipResponse

class UserRelationshipsResponse(BaseModel):
    user_id: str = Field(..., description="User ID")
    as_parent: List[ParentChildRelationshipResponse] = Field(default_factory=list, description="Relationships where user is a parent")
    as_child: List[ParentChildRelationshipResponse] = Field(default_factory=list, description="Relationships where user is a child")
    as_escort: List[ParentChildRelationshipResponse] = Field(default_factory=list, description="Relationships where user is an escort")
    
    class Config:
        from_attributes = True 