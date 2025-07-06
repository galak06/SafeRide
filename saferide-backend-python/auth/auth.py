from fastapi import HTTPException, Depends, status, Request, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import json
import uuid
import os
import logging
from sqlalchemy.orm import Session

from models.base import UserModel, RoleModel, PermissionModel
from models.enums import UserRole, Permission
from db.repositories import UserRepository, RoleRepository, PermissionRepository
from db import get_db
from core.config import settings
from core.exceptions import AuthenticationError, NotFoundError, DatabaseError

# Configure logging
logger = logging.getLogger(__name__)

# Security configuration - Use environment variables
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = 7  # Refresh tokens last 7 days

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token security
security = HTTPBearer(auto_error=False)

# Password utilities
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

# JWT token utilities
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add jti (JWT ID) to ensure uniqueness
    to_encode.update({
        "exp": expire, 
        "type": "access",
        "jti": str(uuid.uuid4()),  # Unique identifier for each token
        "iat": datetime.utcnow()   # Issued at timestamp
    })
    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """Create a JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def verify_refresh_token(token: str) -> Optional[dict]:
    """Verify and decode a refresh token specifically"""
    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            return None
        return payload
    except JWTError:
        return None

# Authentication dependencies
async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> UserModel:
    """Get current authenticated user from database"""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check token type
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = str(payload.get("sub"))
    if not user_id or user_id == "None":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    try:
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Convert to UserModel
        user_model = _convert_db_user_to_model(user, db)
        return user_model
        
    except Exception as e:
        logger.error(f"Error getting user from database: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_active_user(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    return current_user

async def get_current_user_from_cookie(
    access_token: str = Cookie(None),
    db: Session = Depends(get_db)
) -> UserModel:
    """Get current authenticated user from cookie"""
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    payload = verify_token(access_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    # Check token type
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    
    user_id = str(payload.get("sub"))
    if not user_id or user_id == "None":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID"
        )
    
    # Get user from database
    try:
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # Convert to UserModel
        user_model = _convert_db_user_to_model(user, db)
        return user_model
        
    except Exception as e:
        logger.error(f"Error getting user from database: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

async def get_current_active_user_from_cookie(
    current_user: UserModel = Depends(get_current_user_from_cookie)
) -> UserModel:
    """Get current active user from cookie"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    return current_user

async def get_current_user_hybrid(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    access_token: str = Cookie(None),
    db: Session = Depends(get_db)
) -> UserModel:
    """
    Get current authenticated user from either Authorization header or cookie.
    This allows for flexible authentication methods.
    """
    token = None
    
    # First try Authorization header
    if credentials:
        token = credentials.credentials
    # Fall back to cookie
    elif access_token:
        token = access_token
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    # Check token type
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    
    user_id = str(payload.get("sub"))
    if not user_id or user_id == "None":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID"
        )
    
    # Get user from database
    try:
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # Convert to UserModel
        user_model = _convert_db_user_to_model(user, db)
        return user_model
        
    except Exception as e:
        logger.error(f"Error getting user from database: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

async def get_current_active_user_hybrid(
    current_user: UserModel = Depends(get_current_user_hybrid)
) -> UserModel:
    """Get current active user using hybrid authentication"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    return current_user

# Authorization dependencies
def require_permission(permission: str):
    """Decorator to require a specific permission"""
    def permission_dependency(
        current_user: UserModel = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ):
        if not has_permission(current_user, permission, db):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission}' required"
            )
        return current_user
    return permission_dependency

def require_role(role: str):
    """Decorator to require a specific role"""
    def role_dependency(
        current_user: UserModel = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ):
        if not has_role(current_user, role, db):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{role}' required"
            )
        return current_user
    return role_dependency

def require_admin():
    """Decorator to require admin role"""
    return require_role("admin")

def require_manager_or_admin():
    """Decorator to require manager or admin role"""
    def role_dependency(
        current_user: UserModel = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ):
        if not has_role(current_user, "admin", db) and not has_role(current_user, "manager", db):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Manager or admin role required"
            )
        return current_user
    return role_dependency

# Permission checking utilities
def has_permission(user: UserModel, permission: str, db: Session) -> bool:
    """Check if user has a specific permission"""
    try:
        # Get user's roles and their permissions
        user_permissions = get_user_permissions(user, db)
        return permission in user_permissions
    except Exception as e:
        logger.error(f"Error checking permission {permission} for user {user.id}: {str(e)}")
        return False

def has_role(user: UserModel, role: str, db: Session) -> bool:
    """Check if user has a specific role"""
    try:
        # Get user's roles from database
        db_user = UserRepository.get_by_id(db, user.id)
        if not db_user:
            return False
        
        user_roles = [role.name for role in db_user.roles]
        return role in user_roles
    except Exception as e:
        logger.error(f"Error checking role {role} for user {user.id}: {str(e)}")
        return False

def get_user_permissions(user: UserModel, db: Session) -> List[str]:
    """Get all permissions for a user"""
    try:
        # Get user's roles and their permissions from database
        db_user = UserRepository.get_by_id(db, user.id)
        if not db_user:
            return []
        
        permissions = set()
        for role in db_user.roles:
            for permission in role.permissions:
                permissions.add(permission.name)
        
        return list(permissions)
    except Exception as e:
        logger.error(f"Error getting permissions for user {user.id}: {str(e)}")
        return []

# Utility functions
def _convert_db_user_to_model(db_user, db: Session) -> UserModel:
    """Convert database user object to UserModel"""
    try:
        # Get user's roles
        roles = []
        if hasattr(db_user, 'roles') and db_user.roles:
            for role in db_user.roles:
                role_model = RoleModel(
                    id=role.id,
                    name=role.name,
                    description=role.description or "",
                    permissions=[],  # Will be populated if needed
                    is_active=True,
                    created_at=role.created_at,
                    updated_at=role.updated_at or role.created_at
                )
                roles.append(role_model)
        
        # Create UserModel
        user_model = UserModel(
            id=db_user.id,
            email=db_user.email,
            password_hash=db_user.hashed_password,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            phone=db_user.phone,
            role_id=roles[0].id if roles else "",
            company_id=None,  # Will be populated if user has company
            is_active=db_user.is_active,
            is_verified=db_user.is_verified,
            profile_picture=None,  # Not implemented in current User model
            created_at=db_user.created_at,
            updated_at=db_user.updated_at or db_user.created_at,
            last_login=db_user.last_login,
            parent_ids=[],  # Will be populated from relationships
            child_ids=[],   # Will be populated from relationships
            escort_ids=[],  # Will be populated from relationships
            is_child=False,  # Will be determined from relationships
            is_parent=False, # Will be determined from relationships
            is_escort=False  # Will be determined from relationships
        )
        
        return user_model
        
    except Exception as e:
        logger.error(f"Error converting database user to model: {str(e)}")
        raise DatabaseError(f"Failed to convert user data: {str(e)}")

# Session management utilities
class SessionManager:
    """Manages user sessions and token refresh"""
    
    def __init__(self):
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
    
    def create_session(self, user_id: str, access_token: str, refresh_token: str) -> Dict[str, Any]:
        """Create a new user session"""
        session_data = {
            "user_id": user_id,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow(),
            "is_active": True
        }
        self.active_sessions[user_id] = session_data
        return session_data
    
    def get_session(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user session"""
        session = self.active_sessions.get(user_id)
        if session and session.get("is_active"):
            # Update last activity
            session["last_activity"] = datetime.utcnow()
            return session
        return None
    
    def invalidate_session(self, user_id: str) -> bool:
        """Invalidate user session"""
        if user_id in self.active_sessions:
            self.active_sessions[user_id]["is_active"] = False
            return True
        return False
    
    def refresh_session(self, user_id: str, new_access_token: str) -> Optional[Dict[str, Any]]:
        """Refresh user session with new access token"""
        session = self.get_session(user_id)
        if session:
            session["access_token"] = new_access_token
            session["last_activity"] = datetime.utcnow()
            return session
        return None
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions and return count of cleaned sessions"""
        current_time = datetime.utcnow()
        expired_sessions = []
        
        for user_id, session in self.active_sessions.items():
            # Check if session is older than refresh token expiry
            session_age = current_time - session["created_at"]
            if session_age > timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS):
                expired_sessions.append(user_id)
        
        # Remove expired sessions
        for user_id in expired_sessions:
            del self.active_sessions[user_id]
        
        return len(expired_sessions)

# Global session manager instance
session_manager = SessionManager() 