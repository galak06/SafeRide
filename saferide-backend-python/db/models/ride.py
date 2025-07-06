"""
Ride model for managing transportation rides.
"""

from sqlalchemy import Column, String, DateTime, Float, Integer, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
from .enums import RideStatusEnum

class Ride(Base):
    """SQLAlchemy model for rides"""
    __tablename__ = "rides"

    id = Column(String, primary_key=True, index=True)
    passenger_id = Column(String, ForeignKey("users.id"), nullable=False)
    driver_id = Column(String, ForeignKey("users.id"))
    company_id = Column(String, ForeignKey("driver_companies.id"))
    origin_lat = Column(Float, nullable=False)
    origin_lng = Column(Float, nullable=False)
    origin_address = Column(Text)
    destination_lat = Column(Float, nullable=False)
    destination_lng = Column(Float, nullable=False)
    destination_address = Column(Text)
    status = Column(Enum(RideStatusEnum), default=RideStatusEnum.PENDING)
    passenger_count = Column(Integer, default=1)
    estimated_distance = Column(Float)
    estimated_duration = Column(Integer)
    estimated_fare = Column(Float)
    actual_fare = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    pickup_time = Column(DateTime(timezone=True))
    completion_time = Column(DateTime(timezone=True))
    
    # Relationships
    passenger = relationship("User", foreign_keys=[passenger_id], back_populates="rides_as_passenger")
    driver = relationship("User", foreign_keys=[driver_id], back_populates="rides_as_driver") 