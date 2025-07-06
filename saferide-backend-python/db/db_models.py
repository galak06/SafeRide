"""
Database models - Main import file for backward compatibility.
This file imports all models from the modular structure.
"""

# Import all models for backward compatibility
from .models.enums import UserRoleEnum, RideStatusEnum, CompanyStatusEnum, RelationshipTypeEnum
from .models.associations import user_roles, role_permissions
from .models.user import User
from .models.role import Role
from .models.permission import Permission
from .models.audit_log import AuditLog
from .models.parent_child_relationship import ParentChildRelationship
from .models.child_model import ChildModel
from .models.company import Company

# Export all models
__all__ = [
    'User',
    'Role', 
    'Permission',
    'AuditLog',
    'ParentChildRelationship',
    'ChildModel',
    'Company',
    'UserRoleEnum',
    'RideStatusEnum',
    'CompanyStatusEnum',
    'RelationshipTypeEnum',
    'user_roles',
    'role_permissions'
] 