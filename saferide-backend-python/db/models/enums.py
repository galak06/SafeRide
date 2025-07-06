"""
Enum definitions for database models.
"""

import enum

class UserRoleEnum(str, enum.Enum):
    """Enum for user roles"""
    ADMIN = "admin"
    MANAGER = "manager"
    DRIVER = "driver"
    PASSENGER = "passenger"

class RideStatusEnum(str, enum.Enum):
    """Enum for ride status"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class CompanyStatusEnum(str, enum.Enum):
    """Enum for company status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class RelationshipTypeEnum(str, enum.Enum):
    """Enum for relationship types"""
    PARENT = "parent"
    CHILD = "child"
    ESCORT = "escort" 