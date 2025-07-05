from fastapi import APIRouter, Depends, status, Request, Response, HTTPException, Cookie
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models.requests import LoginRequest
from models.responses import LoginResponse, UserResponse
from services.auth_service import AuthService
from db import get_db
from auth.auth import get_current_active_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login", response_model=UserResponse)
async def login(login_request: LoginRequest, request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Authenticate a user and set JWT as HTTP-only cookie.
    """
    client_ip = request.client.host if request.client else "unknown"
    auth_service = AuthService(db)
    login_result = auth_service.authenticate_user(login_request, client_ip)
    # Set JWT as HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=login_result.access_token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=login_result.expires_in
    )
    return login_result.user

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    access_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    """
    Get current user info from JWT in cookie.
    """
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    auth_service = AuthService(db)
    from jose import JWTError, jwt
    from core.config import settings
    
    try:
        # Decode and validate JWT token
        payload = jwt.decode(access_token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token: missing user ID")
        
        # Check if user exists before proceeding
        from db.repositories import UserRepository
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        # Check if user is active
        if not getattr(user, 'is_active', True):
            raise HTTPException(status_code=401, detail="User account is inactive")
        
        # Get user info from service
        return auth_service.get_current_user_info(user_id)
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log unexpected errors and return 500
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Unexpected error in get_current_user_info: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/logout")
async def logout(response: Response):
    """
    Clear the authentication cookie.
    """
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"} 