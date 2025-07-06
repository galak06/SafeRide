from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from models.entities.child import ChildCreate, ChildUpdate, ChildResponse
from services.child_service import ChildService
from db import get_db
from auth.auth import get_current_active_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/children", tags=["Children"])

@router.post("/", response_model=ChildResponse, status_code=status.HTTP_201_CREATED)
async def create_child(
    child_data: ChildCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new child in the system
    """
    try:
        child_service = ChildService(db)
        return child_service.create_child(child_data)
    except Exception as e:
        logger.error(f"Failed to create child: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create child: {str(e)}"
        )

@router.get("/", response_model=List[ChildResponse])
async def get_all_children(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all active children in the system
    """
    try:
        child_service = ChildService(db)
        return child_service.get_all_children()
    except Exception as e:
        logger.error(f"Failed to get all children: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get children: {str(e)}"
        )

@router.get("/{child_id}", response_model=ChildResponse)
async def get_child(
    child_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific child by ID
    """
    try:
        child_service = ChildService(db)
        child = child_service.get_child_by_id(child_id)
        
        if not child:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Child with ID {child_id} not found"
            )
        
        return child
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get child {child_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get child: {str(e)}"
        )

@router.get("/parent/{parent_id}", response_model=List[ChildResponse])
async def get_children_by_parent(
    parent_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all children for a specific parent
    """
    try:
        child_service = ChildService(db)
        return child_service.get_children_by_parent(parent_id)
    except Exception as e:
        logger.error(f"Failed to get children for parent {parent_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get children: {str(e)}"
        )

@router.put("/{child_id}", response_model=ChildResponse)
async def update_child(
    child_id: str,
    child_data: ChildUpdate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a child's information
    """
    try:
        child_service = ChildService(db)
        return child_service.update_child(child_id, child_data)
    except Exception as e:
        logger.error(f"Failed to update child {child_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update child: {str(e)}"
        )

@router.delete("/{child_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_child(
    child_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a child (soft delete)
    """
    try:
        child_service = ChildService(db)
        child_service.delete_child(child_id)
        return None
    except Exception as e:
        logger.error(f"Failed to delete child {child_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete child: {str(e)}"
        )

@router.get("/search/", response_model=List[ChildResponse])
async def search_children(
    q: str = Query(..., description="Search term for child name or email"),
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Search children by name or email
    """
    try:
        child_service = ChildService(db)
        return child_service.search_children(q)
    except Exception as e:
        logger.error(f"Failed to search children: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search children: {str(e)}"
        ) 