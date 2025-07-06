from sqlalchemy import Column, String, Text, Boolean, DateTime, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from ..database import Base

class Company(Base):
    """Company model for ride-sharing companies"""
    __tablename__ = "companies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    contact_email = Column(String(255), nullable=False)
    contact_phone = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    
    # Operation area - support both circle and polygon
    operation_area_type = Column(String(20), nullable=False, default="circle")  # "circle" or "polygon"
    # For circle: center_lat, center_lng, radius_km
    center_lat = Column(Float, nullable=True)
    center_lng = Column(Float, nullable=True)
    radius_km = Column(Float, nullable=True)
    # For polygon: coordinates as JSON array of {lat, lng} objects
    polygon_coordinates = Column(JSON, nullable=True)
    
    # Company status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    drivers = relationship("User", back_populates="company", foreign_keys="User.company_id")
    
    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}')>" 