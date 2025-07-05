from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class RelationshipType(str, Enum):
    PARENT = "parent"
    CHILD = "child"
    ESCORT = "escort"

class ParentChildRelationship(BaseModel):
    id: str = Field(..., description="Relationship ID")
    parent_id: str = Field(..., description="Parent user ID")
    child_id: str = Field(..., description="Child user ID")
    escort_id: Optional[str] = Field(None, description="Escort user ID (if assigned)")
    relationship_type: RelationshipType = Field(..., description="Type of relationship")
    is_active: bool = Field(True, description="Whether relationship is active")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = Field(None, description="Additional notes about the relationship")

class ParentChildRelationshipCreate(BaseModel):
    parent_id: str = Field(..., description="Parent user ID")
    child_id: str = Field(..., description="Child user ID")
    escort_id: Optional[str] = Field(None, description="Escort user ID")
    relationship_type: RelationshipType = Field(..., description="Type of relationship")
    notes: Optional[str] = Field(None, description="Additional notes")

class ParentChildRelationshipUpdate(BaseModel):
    escort_id: Optional[str] = Field(None, description="Escort user ID")
    is_active: Optional[bool] = Field(None, description="Whether relationship is active")
    notes: Optional[str] = Field(None, description="Additional notes")

class UserRelationships(BaseModel):
    user_id: str = Field(..., description="User ID")
    as_parent: List[ParentChildRelationship] = Field(default_factory=list, description="Relationships where user is parent")
    as_child: List[ParentChildRelationship] = Field(default_factory=list, description="Relationships where user is child")
    as_escort: List[ParentChildRelationship] = Field(default_factory=list, description="Relationships where user is escort") 