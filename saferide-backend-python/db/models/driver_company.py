"""
DriverCompany model for managing transportation companies.
"""

from sqlalchemy import Column, String, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
from .enums import CompanyStatusEnum
from .associations import company_drivers

class DriverCompany(Base):
    """SQLAlchemy model for driver companies"""
    __tablename__ = "driver_companies"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    address = Column(Text)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    country = Column(String, default="USA")
    status = Column(Enum(CompanyStatusEnum), default=CompanyStatusEnum.ACTIVE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    service_areas = relationship("ServiceArea", back_populates="company")
    drivers = relationship("User", secondary=company_drivers) 