from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from models.base.user_model import UserModel
from models.responses.user_response import UserResponse
from models.base.role_model import RoleModel
from core.exceptions import NotFoundError

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        """Get user by ID"""
        # Mock data for now - replace with actual database queries
        mock_users = {
            "admin-001": UserResponse(
                id="admin-001",
                email="admin@saferide.com",
                first_name="Admin",
                last_name="User",
                phone="+1234567890",
                role=RoleModel(
                    id="role-1", 
                    name="admin", 
                    description="Administrator",
                    permissions=["read", "write", "admin"],
                    is_active=True
                ),
                company=None,
                is_active=True,
                is_verified=True,
                profile_picture=None,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                last_login=datetime.now()
            ),
            "child-001": UserResponse(
                id="child-001",
                email="child1@example.com",
                first_name="Child",
                last_name="One",
                phone="+1234567891",
                role=RoleModel(
                    id="role-2", 
                    name="child", 
                    description="Child user",
                    permissions=["read"],
                    is_active=True
                ),
                company=None,
                is_active=True,
                is_verified=True,
                profile_picture=None,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                last_login=datetime.now()
            ),
            "child-002": UserResponse(
                id="child-002",
                email="child2@example.com",
                first_name="Child",
                last_name="Two",
                phone="+1234567892",
                role=RoleModel(
                    id="role-2", 
                    name="child", 
                    description="Child user",
                    permissions=["read"],
                    is_active=True
                ),
                company=None,
                is_active=True,
                is_verified=True,
                profile_picture=None,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                last_login=datetime.now()
            ),
            "escort-001": UserResponse(
                id="escort-001",
                email="escort@example.com",
                first_name="Escort",
                last_name="User",
                phone="+1234567893",
                role=RoleModel(
                    id="role-3", 
                    name="escort", 
                    description="Escort user",
                    permissions=["read", "write"],
                    is_active=True
                ),
                company=None,
                is_active=True,
                is_verified=True,
                profile_picture=None,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                last_login=datetime.now()
            )
        }
        
        return mock_users.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Get user by email"""
        # Mock implementation - replace with actual database queries
        mock_users = {
            "admin@saferide.com": UserResponse(
                id="admin-001",
                email="admin@saferide.com",
                first_name="Admin",
                last_name="User",
                phone="+1234567890",
                role=RoleModel(
                    id="role-1", 
                    name="admin", 
                    description="Administrator",
                    permissions=["read", "write", "admin"],
                    is_active=True
                ),
                company=None,
                is_active=True,
                is_verified=True,
                profile_picture=None,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                last_login=datetime.now()
            )
        }
        
        return mock_users.get(email.lower())

    def get_all_users(self) -> list[UserResponse]:
        """Get all users"""
        # Mock implementation - replace with actual database queries
        return [
            UserResponse(
                id="admin-001",
                email="admin@saferide.com",
                first_name="Admin",
                last_name="User",
                phone="+1234567890",
                role=RoleModel(
                    id="role-1", 
                    name="admin", 
                    description="Administrator",
                    permissions=["read", "write", "admin"],
                    is_active=True
                ),
                company=None,
                is_active=True,
                is_verified=True,
                profile_picture=None,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                last_login=datetime.now()
            ),
            UserResponse(
                id="child-001",
                email="child1@example.com",
                first_name="Child",
                last_name="One",
                phone="+1234567891",
                role=RoleModel(
                    id="role-2", 
                    name="child", 
                    description="Child user",
                    permissions=["read"],
                    is_active=True
                ),
                company=None,
                is_active=True,
                is_verified=True,
                profile_picture=None,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                last_login=datetime.now()
            ),
            UserResponse(
                id="child-002",
                email="child2@example.com",
                first_name="Child",
                last_name="Two",
                phone="+1234567892",
                role=RoleModel(
                    id="role-2", 
                    name="child", 
                    description="Child user",
                    permissions=["read"],
                    is_active=True
                ),
                company=None,
                is_active=True,
                is_verified=True,
                profile_picture=None,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                last_login=datetime.now()
            ),
            UserResponse(
                id="escort-001",
                email="escort@example.com",
                first_name="Escort",
                last_name="User",
                phone="+1234567893",
                role=RoleModel(
                    id="role-3", 
                    name="escort", 
                    description="Escort user",
                    permissions=["read", "write"],
                    is_active=True
                ),
                company=None,
                is_active=True,
                is_verified=True,
                profile_picture=None,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                last_login=datetime.now()
            )
        ] 