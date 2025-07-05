from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import re
import html
from typing import Dict, Any
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

class SecurityMiddleware:
    """Security middleware for input sanitization and validation"""
    
    @staticmethod
    def sanitize_input(data: Any) -> Any:
        """Sanitize input data to prevent XSS and injection attacks"""
        if isinstance(data, str):
            # HTML escape to prevent XSS
            data = html.escape(data)
            # Remove potentially dangerous characters
            data = re.sub(r'[<>"\']', '', data)
        elif isinstance(data, dict):
            return {k: SecurityMiddleware.sanitize_input(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [SecurityMiddleware.sanitize_input(item) for item in data]
        return data
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))
    
    @staticmethod
    def validate_password_strength(password: str) -> bool:
        """Validate password strength"""
        if len(password) < 8:
            return False
        # Check for at least one uppercase, lowercase, digit, and special character
        has_upper = re.search(r'[A-Z]', password)
        has_lower = re.search(r'[a-z]', password)
        has_digit = re.search(r'\d', password)
        has_special = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
        return bool(has_upper and has_lower and has_digit and has_special)

class RateLimitMiddleware:
    """Rate limiting middleware with different limits for different endpoints"""
    
    @staticmethod
    def get_rate_limits() -> Dict[str, str]:
        """Define rate limits for different endpoints"""
        return {
            "/api/auth/login": "5/minute",  # Stricter for login
            "/api/auth/register": "3/minute",  # Very strict for registration
            "/api/": "100/minute",  # General API limit
            "/": "1000/minute",  # General limit
        }
    
    @staticmethod
    def get_default_limit() -> str:
        """Default rate limit"""
        return "100/minute"

class SecurityHeadersMiddleware:
    """Add security headers to responses"""
    
    @staticmethod
    def add_security_headers(response: JSONResponse) -> JSONResponse:
        """Add security headers to prevent common attacks"""
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

class InputValidationMiddleware:
    """Input validation middleware"""
    
    @staticmethod
    async def validate_request(request: Request) -> None:
        """Validate incoming request data"""
        # Check content length to prevent large payload attacks
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > 1024 * 1024:  # 1MB limit
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Request payload too large"
            )
        
        # Check for suspicious headers
        suspicious_headers = ["x-forwarded-for", "x-real-ip", "x-forwarded-host"]
        for header in suspicious_headers:
            if header in request.headers:
                logger.warning(f"Suspicious header detected: {header}")
        
        # Validate content type for POST/PUT requests
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "")
            if not content_type.startswith("application/json"):
                raise HTTPException(
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                    detail="Content-Type must be application/json"
                )

class BruteForceProtectionMiddleware:
    """Brute force protection middleware"""
    
    def __init__(self):
        self.failed_attempts: Dict[str, int] = {}
        self.locked_ips: Dict[str, float] = {}
        self.max_attempts = 5
        self.lockout_duration = 300  # 5 minutes
    
    def is_ip_locked(self, ip: str) -> bool:
        """Check if IP is locked due to brute force attempts"""
        if ip in self.locked_ips:
            lockout_time = self.locked_ips[ip]
            if time.time() - lockout_time < self.lockout_duration:
                return True
            else:
                # Remove expired lockout
                del self.locked_ips[ip]
                self.failed_attempts[ip] = 0
        return False
    
    def record_failed_attempt(self, ip: str) -> None:
        """Record a failed authentication attempt"""
        self.failed_attempts[ip] = self.failed_attempts.get(ip, 0) + 1
        
        if self.failed_attempts[ip] >= self.max_attempts:
            self.locked_ips[ip] = time.time()
            logger.warning(f"IP {ip} locked due to brute force attempts")
    
    def record_successful_attempt(self, ip: str) -> None:
        """Record a successful authentication attempt"""
        if ip in self.failed_attempts:
            del self.failed_attempts[ip]
        if ip in self.locked_ips:
            del self.locked_ips[ip]

# Global brute force protection instance
brute_force_protection = BruteForceProtectionMiddleware()

# Import time for brute force protection
import time 