#!/usr/bin/env python3
"""
Script to create an admin user for testing login functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.database import get_db
from db.repositories import UserRepository, RoleRepository
from models.requests import UserCreateRequest
from core.config import get_settings
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_admin_user():
    """Create admin user if it doesn't exist"""
    db = next(get_db())
    
    try:
        # Check if admin user already exists
        existing_user = UserRepository.get_by_email(db, "admin@saferide.com")
        if existing_user:
            print("✅ Admin user already exists")
            return existing_user
        
        # Create admin role if it doesn't exist
        admin_role = RoleRepository.get_by_name(db, "admin")
        if not admin_role:
            admin_role = RoleRepository.create(db, "admin", "Administrator role")
            print("✅ Created admin role")
        
        # Create admin user
        admin_user_data = UserCreateRequest(
            email="admin@saferide.com",
            first_name="Admin",
            last_name="User",
            phone="+1234567890"
        )
        
        hashed_password = hash_password("admin123")
        admin_user = UserRepository.create(db, admin_user_data, hashed_password)
        
        # Assign admin role
        UserRepository.update_role(db, admin_user.id, admin_role.id)
        
        print("✅ Admin user created successfully!")
        print(f"   Email: {admin_user.email}")
        print(f"   Password: admin123")
        print(f"   Role: {admin_role.name}")
        
        return admin_user
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating admin user...")
    create_admin_user()
    print("Done!") 