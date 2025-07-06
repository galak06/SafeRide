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
    User, Role, Permission, AuditLog, ParentChildRelationship, ChildModel,
    UserRoleEnum, RideStatusEnum, CompanyStatusEnum, RelationshipTypeEnum,
    user_roles, role_permissions
)
from .repositories import (
    UserRepository, RoleRepository, PermissionRepository, AuditLogRepository
)

__all__ = [
    # Database connection
    'get_db', 'engine', 'Base',
    
    # Models
    'User', 'Role', 'Permission', 'AuditLog', 'ParentChildRelationship', 'ChildModel',
    'UserRoleEnum', 'RideStatusEnum', 'CompanyStatusEnum', 'RelationshipTypeEnum',
    'user_roles', 'role_permissions',
    
    # Repositories
    'UserRepository', 'RoleRepository', 'PermissionRepository', 'AuditLogRepository'
] 