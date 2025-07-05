from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext
import os
import logging

from db.repositories import UserRepository, RoleRepository
from models.base import UserModel, RoleModel
from models.requests import LoginRequest
from models.responses import LoginResponse, UserResponse
from models.entities import DriverCompany
from core.exceptions import AuthenticationError, NotFoundError, DatabaseError
from core.config import settings
from core.middleware import SecurityMiddleware, brute_force_protection

# Configure logging
logger = logging.getLogger(__name__)

class AuthService:
    """Service for handling authentication and authorization business logic"""
    
    def __init__(self, db: Session):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.settings = settings
    
    def _convert_role_to_model(self, role) -> RoleModel:
        """Convert SQLAlchemy Role object to RoleModel"""
        return RoleModel(
            id=role.id,
            name=role.name,
            description=role.description or "",
            permissions=[],  # Will be populated if needed
            is_active=True,
            created_at=role.created_at,
            updated_at=role.updated_at or role.created_at  # Use created_at if updated_at is None
        )
    
    def authenticate_user(self, login_request: LoginRequest, client_ip: str = "unknown") -> LoginResponse:
        """
        Authenticate a user and return login response
        
        Args:
            login_request: Login credentials
            client_ip: Client IP address for brute force protection
            
        Returns:
            LoginResponse with access token and user info
            
        Raises:
            AuthenticationError: If credentials are invalid or user is inactive
            DatabaseError: If database operation fails
        """
        try:
            # Validate input
            if not SecurityMiddleware.validate_email(login_request.email):
                brute_force_protection.record_failed_attempt(client_ip)
                raise AuthenticationError("Invalid email format")
            
            # Get user by email
            user = UserRepository.get_by_email(self.db, login_request.email)
            if not user:
                brute_force_protection.record_failed_attempt(client_ip)
                raise AuthenticationError("Invalid email or password")
            
            # Verify password
            if not self.pwd_context.verify(login_request.password, getattr(user, 'hashed_password', '')):
                brute_force_protection.record_failed_attempt(client_ip)
                raise AuthenticationError("Invalid email or password")
            
            # Check if user is active
            if not getattr(user, 'is_active', False):
                brute_force_protection.record_failed_attempt(client_ip)
                raise AuthenticationError("User account is inactive")
            
            # Record successful login
            brute_force_protection.record_successful_attempt(client_ip)
            
            # Create access token
            access_token = self.create_access_token(getattr(user, 'id', ''))
            
            # Get user roles (many-to-many relationship)
            user_roles = user.roles
            if not user_roles:
                raise DatabaseError("User has no roles assigned")
            
            # Use the first role for now (in a real app, you might want to handle multiple roles)
            user_role = self._convert_role_to_model(user_roles[0])
            
            # Update last login
            UserRepository.update_last_login(self.db, getattr(user, 'id', ''))
            
            # Log successful login
            logger.info(f"Successful login for user {getattr(user, 'email', '')} from IP {client_ip}")
            
            # Create user response
            user_response = UserResponse(
                id=getattr(user, 'id', ''),
                email=getattr(user, 'email', ''),
                first_name=getattr(user, 'first_name', ''),
                last_name=getattr(user, 'last_name', ''),
                phone=getattr(user, 'phone', None),
                role=user_role,
                company=None,  # Will be populated if user has company
                is_active=getattr(user, 'is_active', False),
                is_verified=getattr(user, 'is_verified', False),
                profile_picture=None,  # Not implemented in current User model
                created_at=getattr(user, 'created_at', datetime.utcnow()),
                updated_at=getattr(user, 'updated_at', datetime.utcnow()),
                last_login=getattr(user, 'last_login', None)
            )
            
            return LoginResponse(
                access_token=access_token,
                token_type="bearer",
                expires_in=self.settings.access_token_expire_minutes * 60,
                user=user_response
            )
            
        except (AuthenticationError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Authentication error for IP {client_ip}: {str(e)}")
            raise DatabaseError(f"Authentication failed: {str(e)}")
    
    def get_current_user_info(self, user_id: str) -> UserResponse:
        """
        Get current user information
        
        Args:
            user_id: User ID from token
            
        Returns:
            UserResponse with user information
            
        Raises:
            NotFoundError: If user not found
            DatabaseError: If database operation fails
        """
        try:
            user = UserRepository.get_by_id(self.db, user_id)
            if not user:
                raise NotFoundError("User not found")
            
            # Get user roles (many-to-many relationship)
            user_roles = user.roles
            if not user_roles:
                raise DatabaseError("User has no roles assigned")
            
            # Use the first role for now (in a real app, you might want to handle multiple roles)
            # Add validation to ensure the role object has required attributes
            first_role = user_roles[0]
            if not hasattr(first_role, 'id') or not hasattr(first_role, 'name'):
                raise DatabaseError("Invalid role object structure")
            
            user_role = self._convert_role_to_model(first_role)
            
            return UserResponse(
                id=getattr(user, 'id', ''),
                email=getattr(user, 'email', ''),
                first_name=getattr(user, 'first_name', ''),
                last_name=getattr(user, 'last_name', ''),
                phone=getattr(user, 'phone', None),
                role=user_role,
                company=None,  # Will be populated if user has company
                is_active=getattr(user, 'is_active', False),
                is_verified=getattr(user, 'is_verified', False),
                profile_picture=None,  # Not implemented in current User model
                created_at=getattr(user, 'created_at', datetime.utcnow()),
                updated_at=getattr(user, 'updated_at', datetime.utcnow()),
                last_login=getattr(user, 'last_login', None)
            )
            
        except (NotFoundError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error getting user info for user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to get user info: {str(e)}")
    
    def create_access_token(self, user_id: str) -> str:
        """
        Create JWT access token
        
        Args:
            user_id: User ID to include in token
            
        Returns:
            JWT token string
        """
        expire = datetime.utcnow() + timedelta(minutes=self.settings.access_token_expire_minutes)
        to_encode = {"sub": user_id, "exp": expire}
        return jwt.encode(to_encode, self.settings.secret_key, algorithm=self.settings.algorithm)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash
        
        Args:
            plain_password: Plain text password
            hashed_password: Hashed password
            
        Returns:
            True if password matches, False otherwise
        """
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """
        Hash a password
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
        """
        # Validate password strength
        if not SecurityMiddleware.validate_password_strength(password):
            raise AuthenticationError(
                "Password must be at least 8 characters long and contain uppercase, lowercase, digit, and special character"
            )
        
        return self.pwd_context.hash(password) 