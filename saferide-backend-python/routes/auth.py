from fastapi import APIRouter, Depends, status, Request, Response, HTTPException, Cookie
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import logging
from typing import Optional
from datetime import datetime
from jose import JWTError, jwt

from models.requests import LoginRequest
from models.responses import LoginResponse, UserResponse, TokenRefreshResponse
from services.auth_service import AuthService
from db import get_db
from auth.auth import get_current_active_user, get_current_active_user_from_cookie, session_manager
from core.exceptions import AuthenticationError, NotFoundError, DatabaseError
from core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login", response_model=LoginResponse)
async def login(
    login_request: LoginRequest, 
    request: Request, 
    response: Response, 
    db: Session = Depends(get_db)
):
    """
    Authenticate a user and return JWT tokens.
    Access token is set as HTTP-only cookie, refresh token is returned in response body.
    """
    try:
        client_ip = request.client.host if request.client else "unknown"
        auth_service = AuthService(db)
        login_result = auth_service.authenticate_user(login_request, client_ip)
        
        # Set access token as HTTP-only cookie
        response.set_cookie(
            key="access_token",
            value=login_result.access_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=login_result.expires_in
        )
        
        # Set refresh token as HTTP-only cookie (for token refresh endpoint)
        response.set_cookie(
            key="refresh_token",
            value=login_result.refresh_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=login_result.refresh_expires_in
        )
        
        logger.info(f"Login successful for user {login_result.user.email}")
        return login_result
        
    except AuthenticationError as e:
        logger.warning(f"Authentication failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except DatabaseError as e:
        logger.error(f"Database error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/refresh", response_model=TokenRefreshResponse)
async def refresh_token(
    request: Request,
    response: Response,
    refresh_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token from cookie.
    """
    try:
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token not found"
            )
        
        client_ip = request.client.host if request.client else "unknown"
        auth_service = AuthService(db)
        refresh_result = auth_service.refresh_access_token(refresh_token, client_ip)
        
        # Set new access token as HTTP-only cookie
        response.set_cookie(
            key="access_token",
            value=refresh_result.access_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=refresh_result.expires_in
        )
        
        logger.info(f"Token refresh successful from IP {client_ip}")
        return refresh_result
        
    except AuthenticationError as e:
        logger.warning(f"Token refresh failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except DatabaseError as e:
        logger.error(f"Database error during token refresh: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error during token refresh: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    request: Request,
    access_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    """
    Get current user info from JWT in cookie.
    """
    try:
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Not authenticated"
            )
        
        auth_service = AuthService(db)
        
        # Decode and validate JWT token
        payload = jwt.decode(access_token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid token: missing user ID"
            )
        
        # Check token type
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid token type"
            )
        
        # Get user info from service
        try:
            user_info = auth_service.get_current_user_info(user_id)
        except NotFoundError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        logger.debug(f"User info retrieved for user {user_id}")
        return user_info
        
    except JWTError:
        logger.warning("Invalid JWT token in /me endpoint")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token"
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_current_user_info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Internal server error"
        )

@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    access_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    """
    Logout user and clear authentication cookies.
    """
    try:
        if access_token:
            # Try to get user ID from token for audit logging
            try:
                payload = jwt.decode(access_token, settings.secret_key, algorithms=[settings.algorithm])
                user_id = payload.get("sub")
                
                if user_id:
                    client_ip = request.client.host if request.client else "unknown"
                    auth_service = AuthService(db)
                    auth_service.logout_user(user_id, client_ip)
                    logger.info(f"User {user_id} logged out from IP {client_ip}")
            except:
                # If token is invalid, just clear cookies
                pass
        
        # Clear authentication cookies
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        
        return {"message": "Logged out successfully"}
        
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        # Still clear cookies even if there's an error
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return {"message": "Logged out successfully"}

@router.get("/sessions/active")
async def get_active_sessions_count(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user_from_cookie)
):
    """
    Get count of active sessions (admin only).
    """
    try:
        # Check if user has admin role
        from auth.auth import has_role
        if not has_role(current_user, "admin", db):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        
        auth_service = AuthService(db)
        active_count = auth_service.get_active_sessions_count()
        
        return {
            "active_sessions": active_count,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting active sessions count: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/sessions/cleanup")
async def cleanup_expired_sessions(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user_from_cookie)
):
    """
    Clean up expired sessions (admin only).
    """
    try:
        # Check if user has admin role
        from auth.auth import has_role
        if not has_role(current_user, "admin", db):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        
        auth_service = AuthService(db)
        cleaned_count = auth_service.cleanup_expired_sessions()
        
        logger.info(f"Cleaned up {cleaned_count} expired sessions")
        
        return {
            "cleaned_sessions": cleaned_count,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cleaning up expired sessions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 