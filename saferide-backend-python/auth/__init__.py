"""
Authentication package for SafeRide backend.

This package contains all authentication and authorization functionality including:
- JWT token management
- Password hashing and verification
- User authentication logic
- Permission and role checking
"""

from .auth import (
    get_password_hash, verify_password, create_access_token, 
    get_current_user, get_current_active_user, verify_token,
    require_permission, require_role, require_admin, require_manager_or_admin,
    has_permission, has_role, get_user_permissions
)

__all__ = [
    'get_password_hash', 'verify_password', 'create_access_token',
    'get_current_user', 'get_current_active_user', 'verify_token',
    'require_permission', 'require_role', 'require_admin', 'require_manager_or_admin',
    'has_permission', 'has_role', 'get_user_permissions'
] 