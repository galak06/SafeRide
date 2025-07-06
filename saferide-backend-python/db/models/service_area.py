"""
ServiceArea model for defining company service coverage areas.
"""

from sqlalchemy import Column, String, Text, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class ServiceArea(Base):
    """SQLAlchemy model for service areas"""
    __tablename__ = "service_areas"

    id = Column(String, primary_key=True, index=True)
    company_id = Column(String, ForeignKey("driver_companies.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    center_lat = Column(Float, nullable=False)
    center_lng = Column(Float, nullable=False)
    radius_km = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    company = relationship("DriverCompany", back_populates="service_areas") 