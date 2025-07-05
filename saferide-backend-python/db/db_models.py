from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float, Text, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum
from datetime import datetime
from typing import List

# Enum for user roles
class UserRoleEnum(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    DRIVER = "driver"
    PASSENGER = "passenger"

# Enum for ride status
class RideStatusEnum(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# Enum for company status
class CompanyStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

# Many-to-many relationship table for user roles
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', String, ForeignKey('users.id'), primary_key=True),
    Column('role_id', String, ForeignKey('roles.id'), primary_key=True)
)

# Many-to-many relationship table for role permissions
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', String, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', String, ForeignKey('permissions.id'), primary_key=True)
)

class User(Base):
    """SQLAlchemy model for users"""
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    audit_logs = relationship("AuditLog", back_populates="user")
    user_locations = relationship("UserLocation", back_populates="user")
    rides_as_passenger = relationship("Ride", foreign_keys="Ride.passenger_id", back_populates="passenger")
    rides_as_driver = relationship("Ride", foreign_keys="Ride.driver_id", back_populates="driver")

class Role(Base):
    """SQLAlchemy model for roles"""
    __tablename__ = "roles"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")

class Permission(Base):
    """SQLAlchemy model for permissions"""
    __tablename__ = "permissions"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    resource = Column(String, nullable=False)
    action = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

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
    drivers = relationship("User", secondary="company_drivers")

# Many-to-many relationship table for company drivers
company_drivers = Table(
    'company_drivers',
    Base.metadata,
    Column('company_id', String, ForeignKey('driver_companies.id'), primary_key=True),
    Column('driver_id', String, ForeignKey('users.id'), primary_key=True)
)

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

class UserLocation(Base):
    """SQLAlchemy model for user locations"""
    __tablename__ = "user_locations"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    address = Column(Text)
    accuracy = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="user_locations")

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

class AuditLog(Base):
    """SQLAlchemy model for audit logs"""
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    action = Column(String, nullable=False)
    resource = Column(String, nullable=False)
    resource_id = Column(String)
    details = Column(Text)
    ip_address = Column(String)
    user_agent = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="audit_logs") 