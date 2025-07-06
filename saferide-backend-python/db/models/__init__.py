"""
Database models package.
This package contains all SQLAlchemy ORM models organized by domain.
"""

# Import all models to make them available
from .enums import UserRoleEnum, RideStatusEnum, CompanyStatusEnum, RelationshipTypeEnum
from .user import User
from .role import Role
from .permission import Permission
from .driver_company import DriverCompany
from .service_area import ServiceArea
from .user_location import UserLocation
from .ride import Ride
from .route_plan import RoutePlan
from .route_stop import RouteStop
from .audit_log import AuditLog
from .parent_child_relationship import ParentChildRelationship

# Import association tables
from .associations import user_roles, role_permissions, company_drivers

__all__ = [
    # Enums
    "UserRoleEnum",
    "RideStatusEnum", 
    "CompanyStatusEnum",
    "RelationshipTypeEnum",
    
    # Models
    "User",
    "Role",
    "Permission",
    "DriverCompany",
    "ServiceArea",
    "UserLocation",
    "Ride",
    "RoutePlan",
    "RouteStop",
    "AuditLog",
    "ParentChildRelationship",
    
    # Association tables
    "user_roles",
    "role_permissions",
    "company_drivers",
] 