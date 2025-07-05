"""
Models package for SafeRide backend.

This package contains all Pydantic models organized by type in separate folders:
- enums/ - Enums like UserRole, Permission
- base/ - Base models like UserModel, RoleModel
- entities/ - Entity models like ServiceArea, DriverCompany
- requests/ - Request models like UserCreateRequest, LoginRequest
- responses/ - Response models like UserResponse, LoginResponse
- dashboard/ - Dashboard and analytics models
- audit/ - Audit log models
- pagination/ - Pagination models
"""

# Enums
from .enums import UserRole, Permission

# Base Models
from .base import UserModel, RoleModel, PermissionModel

# Entity Models
from .entities import (
    ServiceArea, ServiceAreaModel,
    DriverCompany, CompanyModel,
    UserLocation, RoutePlan,
    RouteOptimizationRequest, RouteOptimizationResponse
)

# Request Models
from .requests import (
    UserCreateRequest, UserUpdateRequest,
    CompanyCreateRequest, CompanyUpdateRequest,
    ServiceAreaCreateRequest, ServiceAreaUpdateRequest,
    UserLocationCreateRequest, UserLocationUpdateRequest,
    LoginRequest, RideRequest,
    RoleCreateRequest, RoleUpdateRequest,
    PermissionCreateRequest
)

# Response Models
from .responses import UserResponse, LoginResponse, RideResponse, Location

# Dashboard Models
from .dashboard import (
    DashboardMetrics, UserStats, RideStats,
    RevenueStats, CompanyStats
)

# Audit Models
from .audit import AuditLogModel, AuditLogResponse

# Pagination Models
from .pagination import PaginationParams, PaginatedResponse

__all__ = [
    # Enums
    'UserRole', 'Permission',
    
    # Base Models
    'UserModel', 'RoleModel', 'PermissionModel',
    
    # Entity Models
    'ServiceArea', 'ServiceAreaModel',
    'DriverCompany', 'CompanyModel',
    'UserLocation', 'RoutePlan',
    'RouteOptimizationRequest', 'RouteOptimizationResponse',
    
    # Request Models
    'UserCreateRequest', 'UserUpdateRequest',
    'CompanyCreateRequest', 'CompanyUpdateRequest',
    'ServiceAreaCreateRequest', 'ServiceAreaUpdateRequest',
    'UserLocationCreateRequest', 'UserLocationUpdateRequest',
    'LoginRequest', 'RideRequest',
    'RoleCreateRequest', 'RoleUpdateRequest',
    'PermissionCreateRequest',
    
    # Response Models
    'UserResponse', 'LoginResponse', 'RideResponse', 'Location',
    
    # Dashboard Models
    'DashboardMetrics', 'UserStats', 'RideStats',
    'RevenueStats', 'CompanyStats',
    
    # Audit Models
    'AuditLogModel', 'AuditLogResponse',
    
    # Pagination Models
    'PaginationParams', 'PaginatedResponse'
] 