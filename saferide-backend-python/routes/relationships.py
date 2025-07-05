from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.requests.parent_child_relationship_request import ParentChildRelationshipCreate, ParentChildRelationshipUpdate
from models.responses.parent_child_relationship_response import ParentChildRelationshipResponse
from services.relationship_service import RelationshipService
from db import get_db
from auth.auth import get_current_active_user

router = APIRouter(prefix="/api/relationships", tags=["Relationships"])

@router.post("/", response_model=ParentChildRelationshipResponse)
async def create_relationship(
    relationship_data: ParentChildRelationshipCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new parent-child relationship
    """
    relationship_service = RelationshipService(db)
    return relationship_service.create_relationship(relationship_data)

@router.get("/{relationship_id}", response_model=ParentChildRelationshipResponse)
async def get_relationship(
    relationship_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific relationship by ID
    """
    relationship_service = RelationshipService(db)
    # For now, return mock data - implement actual database query later
    relationships = relationship_service.get_user_relationships("admin-001")
    relationship = next((rel for rel in relationships if rel.id == relationship_id), None)
    
    if not relationship:
        raise HTTPException(status_code=404, detail="Relationship not found")
    
    return relationship

@router.put("/{relationship_id}", response_model=ParentChildRelationshipResponse)
async def update_relationship(
    relationship_id: str,
    updates: ParentChildRelationshipUpdate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing relationship
    """
    relationship_service = RelationshipService(db)
    return relationship_service.update_relationship(relationship_id, updates)

@router.delete("/{relationship_id}")
async def delete_relationship(
    relationship_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a relationship
    """
    relationship_service = RelationshipService(db)
    relationship_service.delete_relationship(relationship_id)
    return {"message": "Relationship deleted successfully"} 