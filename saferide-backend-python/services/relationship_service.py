from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from db.db_models import ParentChildRelationship
from models.requests.parent_child_relationship_request import ParentChildRelationshipCreate, ParentChildRelationshipUpdate
from models.responses.parent_child_relationship_response import ParentChildRelationshipResponse
from core.exceptions import NotFoundError
from sqlalchemy import or_

class RelationshipService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_relationships(self, user_id: str) -> List[ParentChildRelationshipResponse]:
        """Get all relationships for a specific user from the database"""
        # Query the database for relationships where the user is parent, child, or escort
        relationships = self.db.query(ParentChildRelationship).filter(
            or_(
                ParentChildRelationship.parent_id == user_id,
                ParentChildRelationship.child_id == user_id,
                ParentChildRelationship.escort_id == user_id
            )
        ).all()

        # Convert ORM objects to response models
        response = []
        for rel in relationships:
            response.append(ParentChildRelationshipResponse(
                id=rel.id,
                parent_id=rel.parent_id,
                child_id=rel.child_id,
                escort_id=rel.escort_id,
                relationship_type=rel.relationship_type.value if rel.relationship_type else "parent",
                is_active=rel.is_active,
                created_at=rel.created_at,
                updated_at=rel.updated_at
            ))
        return response

    def get_parent_relationships(self, user_id: str) -> List[ParentChildRelationshipResponse]:
        """Get all relationships where user is a parent"""
        all_relationships = self.get_user_relationships(user_id)
        return [rel for rel in all_relationships if rel.parent_id == user_id]

    def get_child_relationships(self, user_id: str) -> List[ParentChildRelationshipResponse]:
        """Get all relationships where user is a child"""
        all_relationships = self.get_user_relationships(user_id)
        return [rel for rel in all_relationships if rel.child_id == user_id]

    def get_escort_relationships(self, user_id: str) -> List[ParentChildRelationshipResponse]:
        """Get all relationships where user is an escort"""
        all_relationships = self.get_user_relationships(user_id)
        return [rel for rel in all_relationships if rel.escort_id == user_id]

    def create_relationship(self, relationship_data: ParentChildRelationshipCreate) -> ParentChildRelationshipResponse:
        """Create a new parent-child relationship"""
        # Mock implementation - replace with actual database operations
        new_relationship = ParentChildRelationshipResponse(
            id=f"rel-{len(self.get_user_relationships(relationship_data.parent_id)) + 1}",
            parent_id=relationship_data.parent_id,
            child_id=relationship_data.child_id,
            escort_id=relationship_data.escort_id,
            relationship_type=relationship_data.relationship_type,
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        return new_relationship

    def update_relationship(self, relationship_id: str, updates: ParentChildRelationshipUpdate) -> ParentChildRelationshipResponse:
        """Update an existing relationship"""
        # Mock implementation - replace with actual database operations
        relationships = self.get_user_relationships("admin-001")  # Mock data source
        relationship = next((rel for rel in relationships if rel.id == relationship_id), None)
        
        if not relationship:
            raise NotFoundError(f"Relationship {relationship_id} not found")
        
        # Update fields
        if updates.escort_id is not None:
            relationship.escort_id = updates.escort_id
        if updates.relationship_type is not None:
            relationship.relationship_type = updates.relationship_type
        if updates.is_active is not None:
            relationship.is_active = updates.is_active
        
        relationship.updated_at = datetime.now()
        
        return relationship

    def delete_relationship(self, relationship_id: str) -> bool:
        """Delete a relationship"""
        # Mock implementation - replace with actual database operations
        relationships = self.get_user_relationships("admin-001")  # Mock data source
        relationship = next((rel for rel in relationships if rel.id == relationship_id), None)
        
        if not relationship:
            raise NotFoundError(f"Relationship {relationship_id} not found")
        
        return True 