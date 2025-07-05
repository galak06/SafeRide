"""
Database package for SafeRide backend.

This package contains all database-related functionality including:
- Database connection and session management
- Database models and schemas
- Repository pattern implementations
- Database initialization scripts
"""

from .database import get_db, engine, Base
from .db_models import (
    User, Role, Permission, DriverCompany, ServiceArea, UserLocation,
    Ride, RoutePlan, RouteStop, AuditLog, UserRoleEnum, RideStatusEnum,
    CompanyStatusEnum
)
from .repositories import (
    UserRepository, RoleRepository, PermissionRepository, CompanyRepository,
    ServiceAreaRepository, UserLocationRepository, RideRepository, AuditLogRepository
)

__all__ = [
    # Database connection
    'get_db', 'engine', 'Base',
    
    # Models
    'User', 'Role', 'Permission', 'DriverCompany', 'ServiceArea', 'UserLocation',
    'Ride', 'RoutePlan', 'RouteStop', 'AuditLog', 'UserRoleEnum', 'RideStatusEnum',
    'CompanyStatusEnum',
    
    # Repositories
    'UserRepository', 'RoleRepository', 'PermissionRepository', 'CompanyRepository',
    'ServiceAreaRepository', 'UserLocationRepository', 'RideRepository', 'AuditLogRepository'
] 