from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
from .database import get_db
from .db_models import (
    User, Role, Permission, AuditLog, ParentChildRelationship, ChildModel,
    UserRoleEnum, RideStatusEnum, CompanyStatusEnum, RelationshipTypeEnum
)
from models.requests import (
    UserCreateRequest, UserUpdateRequest
)

class UserRepository:
    """Repository for user operations"""
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_by_id(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, 
                search: Optional[str] = None, role_id: Optional[str] = None,
                is_active: Optional[bool] = None) -> List[User]:
        """Get all users with filtering"""
        query = db.query(User)
        
        if search:
            search_filter = or_(
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if role_id:
            query = query.join(User.roles).filter(Role.id == role_id)
        
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, user_data: UserCreateRequest, hashed_password: str) -> User:
        """Create new user"""
        user = User(
            id=str(uuid.uuid4()),
            email=user_data.email,
            hashed_password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone=user_data.phone
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def update(db: Session, user_id: str, user_data: UserUpdateRequest) -> Optional[User]:
        """Update user"""
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            return None
        
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def delete(db: Session, user_id: str) -> bool:
        """Delete user"""
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            return False
        
        db.delete(user)
        db.commit()
        return True
    
    @staticmethod
    def update_last_login(db: Session, user_id: str) -> None:
        """Update user's last login time"""
        user = UserRepository.get_by_id(db, user_id)
        if user:
            setattr(user, 'last_login', datetime.utcnow())
            db.commit()
    
    @staticmethod
    def update_status(db: Session, user_id: str, is_active: bool) -> Optional[User]:
        """Update user active status"""
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            return None
        
        setattr(user, 'is_active', is_active)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def update_role(db: Session, user_id: str, role_id: str) -> Optional[User]:
        """Update user role"""
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            return None
        
        # Get the new role
        role = RoleRepository.get_by_id(db, role_id)
        if not role:
            return None
        
        # Clear existing roles and assign new one
        user.roles = [role]
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def count_all(db: Session) -> int:
        """Count total number of users"""
        return db.query(User).count()
    
    @staticmethod
    def count_active(db: Session) -> int:
        """Count number of active users"""
        return db.query(User).filter(User.is_active == True).count()
    
    @staticmethod
    def get_recent(db: Session, limit: int = 5) -> List[User]:
        """Get recent users"""
        return db.query(User).order_by(desc(User.created_at)).limit(limit).all()

class RoleRepository:
    """Repository for role operations"""
    
    @staticmethod
    def get_by_id(db: Session, role_id: str) -> Optional[Role]:
        """Get role by ID"""
        return db.query(Role).filter(Role.id == role_id).first()
    
    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Role]:
        """Get role by name"""
        return db.query(Role).filter(Role.name == name).first()
    
    @staticmethod
    def get_all(db: Session) -> List[Role]:
        """Get all roles"""
        return db.query(Role).all()
    
    @staticmethod
    def create(db: Session, name: str, description: Optional[str] = None) -> Role:
        """Create new role"""
        role = Role(
            id=str(uuid.uuid4()),
            name=name,
            description=description
        )
        db.add(role)
        db.commit()
        db.refresh(role)
        return role

class PermissionRepository:
    """Repository for permission operations"""
    
    @staticmethod
    def get_by_id(db: Session, permission_id: str) -> Optional[Permission]:
        """Get permission by ID"""
        return db.query(Permission).filter(Permission.id == permission_id).first()
    
    @staticmethod
    def get_all(db: Session) -> List[Permission]:
        """Get all permissions"""
        return db.query(Permission).all()
    
    @staticmethod
    def create(db: Session, permission_id: str, name: str, description: str, 
               resource: str, action: str) -> Permission:
        """Create new permission"""
        permission = Permission(
            id=permission_id,
            name=name,
            description=description,
            resource=resource,
            action=action
        )
        db.add(permission)
        db.commit()
        db.refresh(permission)
        return permission

class AuditLogRepository:
    """Repository for audit log operations"""
    
    @staticmethod
    def create(db: Session, user_id: str, action: str, resource: str,
               resource_id: Optional[str] = None, details: Optional[str] = None,
               ip_address: str = "127.0.0.1", user_agent: str = "Unknown") -> AuditLog:
        """Create new audit log entry"""
        audit_log = AuditLog(
            id=str(uuid.uuid4()),
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            timestamp=datetime.utcnow()
        )
        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)
        return audit_log
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100,
                user_id: Optional[str] = None, action: Optional[str] = None,
                resource: Optional[str] = None) -> List[AuditLog]:
        """Get all audit logs with filtering"""
        query = db.query(AuditLog)
        
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        
        if action:
            query = query.filter(AuditLog.action == action)
        
        if resource:
            query = query.filter(AuditLog.resource == resource)
        
        return query.order_by(desc(AuditLog.timestamp)).offset(skip).limit(limit).all() 