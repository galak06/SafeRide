from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SafeRideException(Exception):
    """Base exception for SafeRide application"""
    def __init__(self, message: str, error_code: str = "UNKNOWN_ERROR", status_code: int = 500):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(self.message)

class AuthenticationError(SafeRideException):
    """Authentication related errors"""
    def __init__(self, message: str = "Authentication failed", error_code: str = "AUTH_001"):
        super().__init__(message, error_code, 401)

class AuthorizationError(SafeRideException):
    """Authorization related errors"""
    def __init__(self, message: str = "Insufficient permissions", error_code: str = "AUTH_002"):
        super().__init__(message, error_code, 403)

class ValidationError(SafeRideException):
    """Data validation errors"""
    def __init__(self, message: str = "Validation failed", error_code: str = "VAL_001"):
        super().__init__(message, error_code, 422)

class NotFoundError(SafeRideException):
    """Resource not found errors"""
    def __init__(self, message: str = "Resource not found", error_code: str = "NOT_FOUND_001"):
        super().__init__(message, error_code, 404)

class DatabaseError(SafeRideException):
    """Database related errors"""
    def __init__(self, message: str = "Database operation failed", error_code: str = "DB_001"):
        super().__init__(message, error_code, 500)

async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for all unhandled exceptions"""
    
    # Log the exception
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    # Handle SafeRide exceptions
    if isinstance(exc, SafeRideException):
        error_response = {
            "error": {
                "message": exc.message,
                "code": exc.error_code,
                "timestamp": datetime.utcnow().isoformat(),
                "status_code": exc.status_code
            }
        }
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response
        )
    
    # Handle all other exceptions
    error_response = {
        "error": {
            "message": "Internal server error",
            "code": "INTERNAL_ERROR",
            "timestamp": datetime.utcnow().isoformat(),
            "status_code": 500
        }
    }
    
    return JSONResponse(
        status_code=500,
        content=error_response
    ) 