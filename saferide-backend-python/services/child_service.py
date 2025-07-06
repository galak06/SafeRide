from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from db.models.child_model import ChildModel
from models.entities.child import ChildCreate, ChildUpdate, ChildResponse
from core.exceptions import NotFoundError, DatabaseError
import logging

logger = logging.getLogger(__name__)

class ChildService:
    """Service for managing children in the system"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_child(self, child_data: ChildCreate) -> ChildResponse:
        """Create a new child in the system"""
        try:
            # Create new child instance
            db_child = ChildModel(
                first_name=child_data.first_name,
                last_name=child_data.last_name,
                email=child_data.email,
                phone=child_data.phone,
                parent_id=child_data.parent_id,
                date_of_birth=child_data.date_of_birth,
                grade=child_data.grade,
                school=child_data.school,
                emergency_contact=child_data.emergency_contact,
                notes=child_data.notes,
                is_active=True
            )
            
            # Add to database
            self.db.add(db_child)
            self.db.commit()
            self.db.refresh(db_child)
            
            logger.info(f"Created child: {db_child.id} for parent: {child_data.parent_id}")
            return ChildResponse.model_validate(db_child)
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create child: {str(e)}")
            raise DatabaseError(f"Failed to create child: {str(e)}")
    
    def get_child_by_id(self, child_id: str) -> Optional[ChildResponse]:
        """Get a child by ID"""
        try:
            db_child = self.db.query(ChildModel).filter(
                ChildModel.id == child_id
            ).first()
            
            if not db_child:
                return None
                
            return ChildResponse.model_validate(db_child)
            
        except Exception as e:
            logger.error(f"Failed to get child {child_id}: {str(e)}")
            raise DatabaseError(f"Failed to get child: {str(e)}")
    
    def get_children_by_parent(self, parent_id: str) -> List[ChildResponse]:
        """Get all children for a specific parent"""
        try:
            db_children = self.db.query(ChildModel).filter(
                and_(
                    ChildModel.parent_id == parent_id,
                    ChildModel.is_active == True
                )
            ).all()
            
            return [ChildResponse.model_validate(child) for child in db_children]
            
        except Exception as e:
            logger.error(f"Failed to get children for parent {parent_id}: {str(e)}")
            raise DatabaseError(f"Failed to get children: {str(e)}")
    
    def get_all_children(self) -> List[ChildResponse]:
        """Get all active children in the system"""
        try:
            db_children = self.db.query(ChildModel).filter(
                ChildModel.is_active == True
            ).all()
            
            return [ChildResponse.model_validate(child) for child in db_children]
            
        except Exception as e:
            logger.error(f"Failed to get all children: {str(e)}")
            raise DatabaseError(f"Failed to get children: {str(e)}")
    
    def update_child(self, child_id: str, child_data: ChildUpdate) -> ChildResponse:
        """Update a child's information"""
        try:
            db_child = self.db.query(ChildModel).filter(
                ChildModel.id == child_id
            ).first()
            
            if not db_child:
                raise NotFoundError(f"Child with ID {child_id} not found")
            
            # Update only provided fields
            update_data = child_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_child, field, value)
            
            self.db.commit()
            self.db.refresh(db_child)
            
            logger.info(f"Updated child: {child_id}")
            return ChildResponse.model_validate(db_child)
            
        except NotFoundError:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to update child {child_id}: {str(e)}")
            raise DatabaseError(f"Failed to update child: {str(e)}")
    
    def delete_child(self, child_id: str) -> bool:
        """Delete a child (soft delete by setting is_active to False)"""
        try:
            db_child = self.db.query(ChildModel).filter(
                ChildModel.id == child_id
            ).first()
            
            if not db_child:
                raise NotFoundError(f"Child with ID {child_id} not found")
            
            # Soft delete
            db_child.is_active = False
            self.db.commit()
            
            logger.info(f"Deleted child: {child_id}")
            return True
            
        except NotFoundError:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to delete child {child_id}: {str(e)}")
            raise DatabaseError(f"Failed to delete child: {str(e)}")
    
    def search_children(self, search_term: str) -> List[ChildResponse]:
        """Search children by name or email"""
        try:
            db_children = self.db.query(ChildModel).filter(
                and_(
                    ChildModel.is_active == True,
                    (
                        ChildModel.first_name.ilike(f"%{search_term}%") |
                        ChildModel.last_name.ilike(f"%{search_term}%") |
                        ChildModel.email.ilike(f"%{search_term}%")
                    )
                )
            ).all()
            
            return [ChildResponse.model_validate(child) for child in db_children]
            
        except Exception as e:
            logger.error(f"Failed to search children: {str(e)}")
            raise DatabaseError(f"Failed to search children: {str(e)}") 