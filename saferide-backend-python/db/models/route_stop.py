"""
RouteStop model for individual stops within a route plan.
"""

from sqlalchemy import Column, String, DateTime, Float, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class RouteStop(Base):
    """SQLAlchemy model for route stops"""
    __tablename__ = "route_stops"

    id = Column(String, primary_key=True, index=True)
    route_plan_id = Column(String, ForeignKey("route_plans.id"), nullable=False)
    stop_order = Column(Integer, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    address = Column(Text)
    stop_type = Column(String)  # pickup, dropoff, waypoint
    estimated_time = Column(DateTime(timezone=True))
    
    # Relationships
    route_plan = relationship("RoutePlan", back_populates="stops") 