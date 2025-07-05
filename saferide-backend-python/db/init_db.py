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

from database import engine, SessionLocal
from db_models import Base, User, Role, Permission, UserRoleEnum
from repositories import UserRepository, RoleRepository, PermissionRepository
from auth import get_password_hash
from models.requests import UserCreateRequest
import uuid

# Load environment variables
load_dotenv()

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

def create_initial_permissions():
    """Create initial permissions"""
    print("Creating initial permissions...")
    db = SessionLocal()
    
    try:
        # Define all permissions
        permissions_data = [
            ("view_users", "View Users", "Can view user information", "users", "read"),
            ("create_users", "Create Users", "Can create new users", "users", "create"),
            ("edit_users", "Edit Users", "Can edit user information", "users", "update"),
            ("delete_users", "Delete Users", "Can delete users", "users", "delete"),
            ("block_users", "Block Users", "Can block/unblock users", "users", "block"),
            ("view_rides", "View Rides", "Can view ride information", "rides", "read"),
            ("create_rides", "Create Rides", "Can create new rides", "rides", "create"),
            ("edit_rides", "Edit Rides", "Can edit ride information", "rides", "update"),
            ("cancel_rides", "Cancel Rides", "Can cancel rides", "rides", "cancel"),
            ("assign_drivers", "Assign Drivers", "Can assign drivers to rides", "rides", "assign"),
            ("view_drivers", "View Drivers", "Can view driver information", "drivers", "read"),
            ("approve_drivers", "Approve Drivers", "Can approve driver applications", "drivers", "approve"),
            ("suspend_drivers", "Suspend Drivers", "Can suspend drivers", "drivers", "suspend"),
            ("rate_drivers", "Rate Drivers", "Can rate drivers", "drivers", "rate"),
            ("view_analytics", "View Analytics", "Can view analytics and reports", "analytics", "read"),
            ("export_reports", "Export Reports", "Can export reports", "reports", "export"),
            ("view_revenue", "View Revenue", "Can view revenue information", "revenue", "read"),
            ("manage_settings", "Manage Settings", "Can manage system settings", "settings", "manage"),
            ("view_logs", "View Logs", "Can view system logs", "logs", "read"),
            ("manage_roles", "Manage Roles", "Can manage user roles", "roles", "manage"),
            ("view_live_rides", "View Live Rides", "Can view live ride tracking", "live_rides", "read"),
            ("track_drivers", "Track Drivers", "Can track driver locations", "driver_tracking", "read"),
            ("manage_companies", "Manage Companies", "Can manage driver companies", "companies", "manage"),
            ("view_company_drivers", "View Company Drivers", "Can view drivers in a company", "company_drivers", "read"),
            ("manage_service_areas", "Manage Service Areas", "Can manage service areas", "service_areas", "manage"),
            ("manage_user_locations", "Manage User Locations", "Can manage user locations", "user_locations", "manage"),
            ("plan_routes", "Plan Routes", "Can plan and optimize routes", "routes", "plan"),
            ("view_route_optimization", "View Route Optimization", "Can view route optimization", "route_optimization", "read"),
        ]
        
        for perm_id, name, description, resource, action in permissions_data:
            # Check if permission already exists
            existing = PermissionRepository.get_by_id(db, perm_id)
            if not existing:
                PermissionRepository.create(db, perm_id, name, description, resource, action)
                print(f"  ✅ Created permission: {name}")
            else:
                print(f"  ⏭️  Permission already exists: {name}")
        
        print("✅ Initial permissions created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating permissions: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def create_initial_roles():
    """Create initial roles"""
    print("Creating initial roles...")
    db = SessionLocal()
    
    try:
        # Create roles
        roles_data = [
            ("admin", "Administrator", "Full system access"),
            ("manager", "Manager", "Management access"),
            ("driver", "Driver", "Driver access"),
            ("passenger", "Passenger", "Passenger access"),
        ]
        
        for role_name, description, _ in roles_data:
            existing = RoleRepository.get_by_name(db, role_name)
            if not existing:
                role = RoleRepository.create(db, role_name, description)
                print(f"  ✅ Created role: {role_name}")
            else:
                role = existing
                print(f"  ⏭️  Role already exists: {role_name}")
        
        print("✅ Initial roles created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating roles: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def create_admin_user():
    """Create admin user"""
    print("Creating admin user...")
    db = SessionLocal()
    
    try:
        # Check if admin user already exists
        admin_user = UserRepository.get_by_email(db, "admin@saferide.com")
        if admin_user:
            print("  ⏭️  Admin user already exists")
            return admin_user
        
        # Create admin user
        admin_data = UserCreateRequest(
            email="admin@saferide.com",
            password="admin123",
            first_name="Admin",
            last_name="User",
            phone="+1234567890"
        )
        
        hashed_password = get_password_hash(admin_data.password)
        admin_user = UserRepository.create(db, admin_data, hashed_password)
        
        # Assign admin role
        admin_role = RoleRepository.get_by_name(db, "admin")
        if admin_role:
            admin_user.roles.append(admin_role)
            db.commit()
            print("  ✅ Admin user created and role assigned")
        else:
            print("  ⚠️  Admin role not found, user created without role")
        
        return admin_user
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def main():
    """Main initialization function"""
    print("🚀 Initializing SafeRide Database...")
    print("=" * 50)
    
    try:
        # Create tables
        create_tables()
        
        # Create initial data
        create_initial_permissions()
        create_initial_roles()
        create_admin_user()
        
        print("=" * 50)
        print("✅ Database initialization completed successfully!")
        print("\n📋 Default credentials:")
        print("   Email: admin@saferide.com")
        print("   Password: admin123")
        print("\n🔗 You can now start the application!")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 