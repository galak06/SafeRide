from typing import List, Dict, Any, Optional
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from db.repositories import UserRepository, RoleRepository
from models.base import UserModel, RoleModel
from core.exceptions import NotFoundError, DatabaseError, ValidationError, AuthenticationError

logger = logging.getLogger(__name__)

class AdminService:
    """Service for handling admin operations with database persistence"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # User Management
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get all users with pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of user dictionaries
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            users = UserRepository.get_all(self.db, skip=skip, limit=limit)
            
            user_dicts = []
            for user in users:
                role = RoleRepository.get_by_id(self.db, user.role_id)
                user_dicts.append({
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone": user.phone,
                    "role": role.name if role else "Unknown",
                    "is_active": getattr(user, 'is_active', False),
                    "is_verified": getattr(user, 'is_verified', False),
                    "profile_picture": user.profile_picture,
                    "created_at": getattr(user, 'created_at', None) if getattr(user, 'created_at', None) is not None else None,
                    "updated_at": getattr(user, 'updated_at', None) if getattr(user, 'updated_at', None) is not None else None,
                    "last_login": getattr(user, 'last_login', None) if getattr(user, 'last_login', None) is not None else None
                })
            return user_dicts
            
        except Exception as e:
            logger.error(f"Error getting users: {e}")
            raise DatabaseError(f"Failed to get users: {str(e)}")
    
    def get_user_by_id(self, user_id: str) -> Dict[str, Any]:
        """
        Get user by ID
        
        Args:
            user_id: User identifier
            
        Returns:
            User dictionary with complete information
            
        Raises:
            NotFoundError: If user not found
            DatabaseError: If database operation fails
        """
        try:
            user = UserRepository.get_by_id(self.db, user_id)
            if not user:
                raise NotFoundError(f"User {user_id} not found")
            
            role = RoleRepository.get_by_id(self.db, user.role_id)
            
            return {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "role": role.name if role else "Unknown",
                "is_active": user.is_active,
                "is_verified": user.is_verified,
                "profile_picture": user.profile_picture,
                "created_at": user.created_at.isoformat() if user.created_at is not None else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at is not None else None,
                "last_login": user.last_login.isoformat() if user.last_login is not None else None
            }
            
        except (NotFoundError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            raise DatabaseError(f"Failed to get user: {str(e)}")
    
    def update_user_status(self, user_id: str, is_active: bool) -> Dict[str, Any]:
        """
        Update user active status
        
        Args:
            user_id: User identifier
            is_active: New active status
            
        Returns:
            Updated user dictionary
            
        Raises:
            NotFoundError: If user not found
            DatabaseError: If database operation fails
        """
        try:
            user = UserRepository.update_status(self.db, user_id, is_active)
            if not user:
                raise NotFoundError(f"User {user_id} not found")
            
            logger.info(f"User {user_id} status updated to {'active' if is_active else 'inactive'}")
            
            return self.get_user_by_id(user_id)
            
        except (NotFoundError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error updating user status: {e}")
            raise DatabaseError(f"Failed to update user status: {str(e)}")
    
    def update_user_role(self, user_id: str, role_id: str) -> Dict[str, Any]:
        """
        Update user role
        
        Args:
            user_id: User identifier
            role_id: New role identifier
            
        Returns:
            Updated user dictionary
            
        Raises:
            NotFoundError: If user or role not found
            ValidationError: If role is invalid
            DatabaseError: If database operation fails
        """
        try:
            # Validate role exists
            role = RoleRepository.get_by_id(self.db, role_id)
            if not role:
                raise ValidationError(f"Role {role_id} not found")
            
            user = UserRepository.update_role(self.db, user_id, role_id)
            if not user:
                raise NotFoundError(f"User {user_id} not found")
            
            logger.info(f"User {user_id} role updated to {role_id}")
            
            return self.get_user_by_id(user_id)
            
        except (NotFoundError, ValidationError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error updating user role: {e}")
            raise DatabaseError(f"Failed to update user role: {str(e)}")
    
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """
        Get dashboard statistics
        
        Returns:
            Dictionary with dashboard statistics
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            total_users = UserRepository.count_all(self.db)
            active_users = UserRepository.count_active(self.db)
            recent_users = UserRepository.get_recent(self.db, limit=7)
            
            return {
                "total_users": total_users,
                "active_users": active_users,
                "recent_users": len(recent_users),
                "user_growth": {
                    "daily": 5,  # Mock data
                    "weekly": 25,  # Mock data
                    "monthly": 100  # Mock data
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting dashboard stats: {e}")
            raise DatabaseError(f"Failed to get dashboard stats: {str(e)}") 