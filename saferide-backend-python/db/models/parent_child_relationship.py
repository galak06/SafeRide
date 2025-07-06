"""
ParentChildRelationship model for managing family relationships in the system.
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
from .enums import RelationshipTypeEnum

class ParentChildRelationship(Base):
    """SQLAlchemy model for parent-child relationships"""
    __tablename__ = "parent_child_relationships"

    id = Column(String, primary_key=True, index=True)
    parent_id = Column(String, ForeignKey("users.id"), nullable=False)
    child_id = Column(String, ForeignKey("users.id"), nullable=False)
    escort_id = Column(String, ForeignKey("users.id"), nullable=True)
    relationship_type = Column(Enum(RelationshipTypeEnum), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    notes = Column(Text, nullable=True) 