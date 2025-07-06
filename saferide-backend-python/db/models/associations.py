"""
Association tables for many-to-many relationships.
"""

from sqlalchemy import Column, String, ForeignKey, Table
from ..database import Base

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

# Many-to-many relationship table for company drivers
company_drivers = Table(
    'company_drivers',
    Base.metadata,
    Column('company_id', String, ForeignKey('driver_companies.id'), primary_key=True),
    Column('driver_id', String, ForeignKey('users.id'), primary_key=True)
) 