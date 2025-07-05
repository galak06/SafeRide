from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import json
import uuid
import os
from models.base import UserModel, RoleModel, PermissionModel
from models.enums import UserRole, Permission
from dotenv import load_dotenv
from core.config import Settings

load_dotenv()

# Security configuration - Use environment variables
settings = Settings()
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

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
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# Authentication dependencies
async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> UserModel:
    """Get current authenticated user"""
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
    user_id = str(payload.get("sub"))
    if not user_id or user_id == "None":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Note: This will be replaced by database lookup in the service layer
    # For now, we'll raise an error indicating this needs to be implemented
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="User lookup from database not yet implemented"
    )

async def get_current_active_user(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Authorization dependencies
def require_permission(permission: str):
    """Decorator to require a specific permission"""
    def permission_dependency(current_user: UserModel = Depends(get_current_active_user)):
        # Note: This will be replaced by database lookup in the service layer
        # For now, we'll raise an error indicating this needs to be implemented
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Permission checking from database not yet implemented"
        )
    return permission_dependency

def require_role(role: str):
    """Decorator to require a specific role"""
    def role_dependency(current_user: UserModel = Depends(get_current_active_user)):
        if current_user.role_id != role:
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
    def role_dependency(current_user: UserModel = Depends(get_current_active_user)):
        if current_user.role_id not in ["admin", "manager"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Manager or admin role required"
            )
        return current_user
    return role_dependency

# Permission checking utilities
def has_permission(user: UserModel, permission: str) -> bool:
    """Check if user has a specific permission"""
    # Note: This will be replaced by database lookup in the service layer
    # For now, return False to indicate this needs to be implemented
    return False

def has_role(user: UserModel, role: str) -> bool:
    """Check if user has a specific role"""
    return user.role_id == role

def get_user_permissions(user: UserModel) -> List[str]:
    """Get all permissions for a user"""
    # Note: This will be replaced by database lookup in the service layer
    # For now, return empty list to indicate this needs to be implemented
    return [] 