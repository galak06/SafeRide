from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base
import uuid

class ChildModel(Base):
    """Database model for children in the system"""
    __tablename__ = "children"

    # Primary key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Basic information
    first_name = Column(String(100), nullable=False, index=True)
    last_name = Column(String(100), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    phone = Column(String(20), nullable=True)
    
    # Parent relationship
    parent_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    
    # Academic information
    date_of_birth = Column(String(10), nullable=True)  # YYYY-MM-DD format
    grade = Column(String(50), nullable=True)
    school = Column(String(255), nullable=True)
    
    # Emergency contact
    emergency_contact = Column(String(20), nullable=True)
    
    # Additional information
    notes = Column(Text, nullable=True)
    
    # Status and timestamps
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    parent = relationship("User", back_populates="children", foreign_keys=[parent_id])

    def __repr__(self):
        return f"<Child(id='{self.id}', name='{self.first_name} {self.last_name}', parent_id='{self.parent_id}')>"

    @property
    def full_name(self):
        """Get the full name of the child"""
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        """Convert model to dictionary"""
        created_at_str = None
        updated_at_str = None
        
        try:
            if self.created_at:
                created_at_str = self.created_at.isoformat()
        except:
            pass
            
        try:
            if self.updated_at:
                updated_at_str = self.updated_at.isoformat()
        except:
            pass
        
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "parent_id": self.parent_id,
            "date_of_birth": self.date_of_birth,
            "grade": self.grade,
            "school": self.school,
            "emergency_contact": self.emergency_contact,
            "notes": self.notes,
            "is_active": self.is_active,
            "created_at": created_at_str,
            "updated_at": updated_at_str
        } 