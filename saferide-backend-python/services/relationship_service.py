from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from models.entities.parent_child_relationship import ParentChildRelationship
from models.requests.parent_child_relationship_request import ParentChildRelationshipCreate, ParentChildRelationshipUpdate
from models.responses.parent_child_relationship_response import ParentChildRelationshipResponse
from core.exceptions import NotFoundError

class RelationshipService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_relationships(self, user_id: str) -> List[ParentChildRelationshipResponse]:
        """Get all relationships for a specific user"""
        # Mock data for now - replace with actual database queries
        relationships = [
            ParentChildRelationshipResponse(
                id="rel-1",
                parent_id="admin-001",
                child_id="child-001",
                escort_id="escort-001",
                relationship_type="parent_child",
                is_active=True,
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            ParentChildRelationshipResponse(
                id="rel-2",
                parent_id="admin-001",
                child_id="child-002",
                escort_id=None,
                relationship_type="parent_child",
                is_active=True,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
        
        # Filter relationships where user is parent, child, or escort
        user_relationships = [
            rel for rel in relationships
            if rel.parent_id == user_id or rel.child_id == user_id or rel.escort_id == user_id
        ]
        
        return user_relationships

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