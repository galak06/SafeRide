from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from models.base.user_model import UserModel
from models.entities.parent_child_relationship import ParentChildRelationship
from models.requests.parent_child_relationship_request import ParentChildRelationshipCreate, ParentChildRelationshipUpdate
from models.responses.user_response import UserResponse
from models.responses.parent_child_relationship_response import ParentChildRelationshipResponse
from models.responses.user_relationships_response import UserRelationshipsResponse
from services.user_service import UserService
from services.relationship_service import RelationshipService
from db import get_db
from auth.auth import get_current_active_user

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str, 
    current_user = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    """
    Get user information by ID
    """
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.get("/{user_id}/relationships", response_model=UserRelationshipsResponse)
async def get_user_relationships(
    user_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all relationships for a specific user
    """
    relationship_service = RelationshipService(db)
    all_relationships = relationship_service.get_user_relationships(user_id)
    
    # Categorize relationships
    as_parent = []
    as_child = []
    as_escort = []
    
    for relationship in all_relationships:
        if relationship.parent_id == user_id:
            as_parent.append(relationship)
        elif relationship.child_id == user_id:
            as_child.append(relationship)
        elif relationship.escort_id == user_id:
            as_escort.append(relationship)
    
    return UserRelationshipsResponse(
        user_id=user_id,
        as_parent=as_parent,
        as_child=as_child,
        as_escort=as_escort
    )

@router.get("/{user_id}/relationships/parent", response_model=List[ParentChildRelationshipResponse])
async def get_parent_relationships(
    user_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all relationships where user is a parent
    """
    relationship_service = RelationshipService(db)
    relationships = relationship_service.get_parent_relationships(user_id)
    return relationships

@router.get("/{user_id}/relationships/child", response_model=List[ParentChildRelationshipResponse])
async def get_child_relationships(
    user_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all relationships where user is a child
    """
    relationship_service = RelationshipService(db)
    relationships = relationship_service.get_child_relationships(user_id)
    return relationships

@router.get("/{user_id}/relationships/escort", response_model=List[ParentChildRelationshipResponse])
async def get_escort_relationships(
    user_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all relationships where user is an escort
    """
    relationship_service = RelationshipService(db)
    relationships = relationship_service.get_escort_relationships(user_id)
    return relationships 