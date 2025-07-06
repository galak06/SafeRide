"""
RoutePlan model for managing optimized transportation routes.
"""

from sqlalchemy import Column, String, DateTime, Float, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class RoutePlan(Base):
    """SQLAlchemy model for route plans"""
    __tablename__ = "route_plans"

    id = Column(String, primary_key=True, index=True)
    company_id = Column(String, ForeignKey("driver_companies.id"), nullable=False)
    driver_id = Column(String, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    description = Column(Text)
    total_distance = Column(Float)
    total_duration = Column(Integer)
    stops_count = Column(Integer)
    is_optimized = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    stops = relationship("RouteStop", back_populates="route_plan") 