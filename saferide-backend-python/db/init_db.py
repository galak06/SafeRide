#!/usr/bin/env python3
"""
Database initialization script for SafeRide
Creates tables and initial data
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from db.database import SessionLocal, init_database
from db.repositories import UserRepository, RoleRepository, PermissionRepository
from auth.auth import get_password_hash
import logging

# Configure logging
logger = logging.getLogger(__name__)

def create_roles_and_permissions():
    """Create default roles and permissions"""
    db = SessionLocal()
    try:
        # Create permissions
        permissions = [
            # User management permissions
            ("user_read", "Read user information", "user", "read"),
            ("user_create", "Create new users", "user", "create"),
            ("user_update", "Update user information", "user", "update"),
            ("user_delete", "Delete users", "user", "delete"),
            
            # Ride management permissions
            ("ride_read", "Read ride information", "ride", "read"),
            ("ride_create", "Create new rides", "ride", "create"),
            ("ride_update", "Update ride information", "ride", "update"),
            ("ride_delete", "Delete rides", "ride", "delete"),
            
            # Company management permissions
            ("company_read", "Read company information", "company", "read"),
            ("company_create", "Create new companies", "company", "create"),
            ("company_update", "Update company information", "company", "update"),
            ("company_delete", "Delete companies", "company", "delete"),
            
            # Admin permissions
            ("admin_all", "Full administrative access", "admin", "all"),
            ("session_manage", "Manage user sessions", "session", "manage"),
        ]
        
        created_permissions = {}
        for perm_id, name, resource, action in permissions:
            permission = PermissionRepository.create(
                db, perm_id, name, f"{action} {resource}", resource, action
            )
            created_permissions[perm_id] = permission
            logger.info(f"Created permission: {name}")
        
        # Create roles with permissions
        roles_data = [
            {
                "name": "admin",
                "description": "Administrator with full access",
                "permissions": ["admin_all", "session_manage"]
            },
            {
                "name": "manager",
                "description": "Manager with company management access",
                "permissions": ["user_read", "user_update", "ride_read", "ride_update", "company_read", "company_update"]
            },
            {
                "name": "driver",
                "description": "Driver with ride management access",
                "permissions": ["ride_read", "ride_update", "user_read"]
            },
            {
                "name": "passenger",
                "description": "Passenger with basic access",
                "permissions": ["ride_read", "ride_create", "user_read"]
            }
        ]
        
        created_roles = {}
        for role_data in roles_data:
            role = RoleRepository.create(db, role_data["name"], role_data["description"])
            created_roles[role_data["name"]] = role
            
            # Assign permissions to role
            for perm_id in role_data["permissions"]:
                if perm_id in created_permissions:
                    role.permissions.append(created_permissions[perm_id])
            
            db.commit()
            logger.info(f"Created role: {role_data['name']}")
        
        return created_roles
        
    except Exception as e:
        logger.error(f"Error creating roles and permissions: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def create_test_users():
    """Create test users for development"""
    db = SessionLocal()
    try:
        # Get roles
        admin_role = RoleRepository.get_by_name(db, "admin")
        passenger_role = RoleRepository.get_by_name(db, "passenger")
        driver_role = RoleRepository.get_by_name(db, "driver")
        manager_role = RoleRepository.get_by_name(db, "manager")
        
        if not all([admin_role, passenger_role, driver_role, manager_role]):
            logger.error("Required roles not found. Please run create_roles_and_permissions first.")
            return
        
        # Test users data
        test_users = [
            {
                "email": "admin@saferide.com",
                "password": "password123",
                "first_name": "Admin",
                "last_name": "User",
                "phone": "+1234567890",
                "role": admin_role,
                "is_active": True,
                "is_verified": True
            },
            {
                "email": "child1@example.com",
                "password": "password123",
                "first_name": "Child",
                "last_name": "One",
                "phone": "+1234567891",
                "role": passenger_role,
                "is_active": True,
                "is_verified": True
            },
            {
                "email": "child2@example.com",
                "password": "password123",
                "first_name": "Child",
                "last_name": "Two",
                "phone": "+1234567892",
                "role": passenger_role,
                "is_active": True,
                "is_verified": True
            },
            {
                "email": "escort@example.com",
                "password": "password123",
                "first_name": "Escort",
                "last_name": "User",
                "phone": "+1234567893",
                "role": driver_role,
                "is_active": True,
                "is_verified": True
            },
            {
                "email": "manager@example.com",
                "password": "password123",
                "first_name": "Manager",
                "last_name": "User",
                "phone": "+1234567894",
                "role": manager_role,
                "is_active": True,
                "is_verified": True
            }
        ]
        
        created_users = []
        for user_data in test_users:
            # Check if user already exists
            existing_user = UserRepository.get_by_email(db, user_data["email"])
            if existing_user:
                logger.info(f"User {user_data['email']} already exists, skipping...")
                continue
            
            # Hash password
            hashed_password = get_password_hash(user_data["password"])
            
            # Create user
            from models.requests import UserCreateRequest
            user_create_request = UserCreateRequest(
                email=user_data["email"],
                password=user_data["password"],  # Will be hashed in repository
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                phone=user_data["phone"],
                role_id=user_data["role"].id
            )
            
            user = UserRepository.create(db, user_create_request, hashed_password)
            
            # Assign role
            user.roles = [user_data["role"]]
            
            # Set additional fields
            user.is_active = user_data["is_active"]
            user.is_verified = user_data["is_verified"]
            
            db.commit()
            created_users.append(user)
            logger.info(f"Created test user: {user_data['email']}")
        
        return created_users
        
    except Exception as e:
        logger.error(f"Error creating test users: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def init_database_with_data():
    """Initialize database with all required data"""
    try:
        logger.info("Initializing database...")
        
        # Initialize database tables
        init_database()
        logger.info("Database tables created successfully")
        
        # Create roles and permissions
        logger.info("Creating roles and permissions...")
        create_roles_and_permissions()
        logger.info("Roles and permissions created successfully")
        
        # Create test users
        logger.info("Creating test users...")
        create_test_users()
        logger.info("Test users created successfully")
        
        logger.info("Database initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise

if __name__ == "__main__":
    init_database_with_data() 