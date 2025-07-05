# SafeRide Authentication System

A comprehensive, production-ready authentication system built with FastAPI, PostgreSQL, and modern security practices.

## 🚀 Features

### ✅ **Complete Authentication Implementation**
- **Database User Lookup**: Full integration with PostgreSQL database
- **JWT Token Management**: Access and refresh tokens with proper expiration
- **Session Management**: In-memory session tracking with cleanup
- **Role-Based Authorization**: Flexible role system with permissions
- **Audit Logging**: Comprehensive activity tracking
- **Brute Force Protection**: Rate limiting and IP-based protection

### 🔐 **Security Features**
- **Password Hashing**: bcrypt with salt rounds
- **JWT Security**: Signed tokens with expiration
- **HTTP-Only Cookies**: Secure token storage
- **Input Validation**: Comprehensive request validation
- **CORS Protection**: Cross-origin resource sharing configuration
- **Security Headers**: HTTP security headers
- **Rate Limiting**: API rate limiting with different tiers

### 🏗️ **Architecture**
- **SOLID Principles**: Clean, maintainable code structure
- **Dependency Injection**: Proper separation of concerns
- **Repository Pattern**: Database abstraction layer
- **Service Layer**: Business logic separation
- **Middleware Stack**: Security and validation middleware

## 📋 **API Endpoints**

### Authentication Endpoints
```
POST /api/auth/login           - User login with credentials
POST /api/auth/refresh         - Refresh access token
GET  /api/auth/me             - Get current user information
POST /api/auth/logout          - User logout
GET  /api/auth/sessions/active - Get active sessions count (admin)
POST /api/auth/sessions/cleanup - Clean expired sessions (admin)
```

### Request/Response Examples

#### Login Request
```json
POST /api/auth/login
{
  "email": "admin@saferide.com",
  "password": "password123"
}
```

#### Login Response
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "refresh_expires_in": 604800,
  "user": {
    "id": "user-123",
    "email": "admin@saferide.com",
    "first_name": "Admin",
    "last_name": "User",
    "role": {
      "id": "role-1",
      "name": "admin",
      "description": "Administrator with full access"
    },
    "is_active": true,
    "is_verified": true
  }
}
```

#### Token Refresh Request
```json
POST /api/auth/refresh
# Uses refresh_token from HTTP-only cookie
```

#### Token Refresh Response
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

## 🗄️ **Database Schema**

### Core Tables
- **users**: User accounts and profiles
- **roles**: User roles and permissions
- **permissions**: System permissions
- **audit_logs**: System audit and activity logs

### Relationships
- **User-Role**: Many-to-many relationship
- **Role-Permission**: Many-to-many relationship
- **User-AuditLog**: One-to-many relationship

## 🔧 **Setup Instructions**

### 1. Environment Configuration
Create a `.env` file with required variables:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/saferide_db

# Security
SECRET_KEY=your-super-secret-key-at-least-32-characters-long

# Application
DEBUG=False
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 2. Database Setup
```bash
# Install PostgreSQL dependencies
pip install -r requirements.txt

# Run database initialization
python setup_auth.py
```

### 3. Start the Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🧪 **Testing**

### Run Authentication Tests
```bash
# Run all authentication tests
pytest tests/test_complete_auth.py -v

# Run specific test
pytest tests/test_complete_auth.py::TestCompleteAuthentication::test_login_with_database_lookup -v
```

### Test Coverage
The authentication system includes comprehensive tests for:
- ✅ User login with database lookup
- ✅ Token refresh functionality
- ✅ Session management
- ✅ Role-based authorization
- ✅ Permission-based authorization
- ✅ Error handling and edge cases
- ✅ Security features

## 🔐 **Security Implementation**

### Password Security
```python
# Password hashing with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash(plain_password)
is_valid = pwd_context.verify(plain_password, hashed_password)
```

### JWT Token Security
```python
# Token creation with expiration and type
access_token = create_access_token({"sub": user_id, "type": "access"})
refresh_token = create_refresh_token({"sub": user_id, "type": "refresh"})
```

### Session Management
```python
# Session tracking with cleanup
session_manager.create_session(user_id, access_token, refresh_token)
session_manager.cleanup_expired_sessions()
```

### Brute Force Protection
```python
# IP-based rate limiting
brute_force_protection.record_failed_attempt(client_ip)
brute_force_protection.record_successful_attempt(client_ip)
```

## 🏗️ **Code Architecture**

### Directory Structure
```
auth/
├── auth.py              # Core authentication logic
├── __init__.py
services/
├── auth_service.py      # Business logic service
├── __init__.py
routes/
├── auth.py              # API route handlers
├── __init__.py
db/
├── database.py          # Database connection
├── repositories.py      # Data access layer
├── init_db.py          # Database initialization
├── __init__.py
models/
├── base/               # Base models
├── requests/           # Request models
├── responses/          # Response models
├── __init__.py
core/
├── config.py           # Configuration management
├── middleware.py       # Security middleware
├── exceptions.py       # Custom exceptions
├── __init__.py
tests/
├── test_complete_auth.py  # Authentication tests
├── __init__.py
```

### Key Classes and Functions

#### AuthService
```python
class AuthService:
    def authenticate_user(self, login_request, client_ip) -> LoginResponse
    def refresh_access_token(self, refresh_token, client_ip) -> TokenRefreshResponse
    def logout_user(self, user_id, client_ip) -> bool
    def get_current_user_info(self, user_id) -> UserResponse
```

#### SessionManager
```python
class SessionManager:
    def create_session(self, user_id, access_token, refresh_token) -> Dict
    def get_session(self, user_id) -> Optional[Dict]
    def invalidate_session(self, user_id) -> bool
    def refresh_session(self, user_id, new_access_token) -> Optional[Dict]
    def cleanup_expired_sessions(self) -> int
```

#### Authentication Dependencies
```python
async def get_current_user(credentials, db) -> UserModel
async def get_current_active_user(current_user) -> UserModel
def require_permission(permission: str)
def require_role(role: str)
def require_admin()
```

## 🔄 **Token Flow**

### 1. Login Flow
```
User Login Request
    ↓
Validate Credentials
    ↓
Check User Status (active/verified)
    ↓
Create Access & Refresh Tokens
    ↓
Create Session
    ↓
Set HTTP-Only Cookies
    ↓
Return User Info + Tokens
```

### 2. Token Refresh Flow
```
Token Refresh Request
    ↓
Validate Refresh Token
    ↓
Check User Status
    ↓
Verify Session
    ↓
Create New Access Token
    ↓
Update Session
    ↓
Set New Access Token Cookie
    ↓
Return New Access Token
```

### 3. Authentication Flow
```
Protected Request
    ↓
Extract Access Token from Cookie
    ↓
Validate Token (signature, expiration, type)
    ↓
Lookup User in Database
    ↓
Check User Status
    ↓
Convert to UserModel
    ↓
Return User for Authorization
```

## 🛡️ **Security Best Practices**

### 1. Token Security
- ✅ Access tokens expire in 30 minutes
- ✅ Refresh tokens expire in 7 days
- ✅ Tokens are signed with secret key
- ✅ Tokens include type validation
- ✅ HTTP-only cookies prevent XSS

### 2. Password Security
- ✅ bcrypt hashing with salt
- ✅ Minimum 8 character requirement
- ✅ Password strength validation
- ✅ Secure password comparison

### 3. Session Security
- ✅ Session invalidation on logout
- ✅ Automatic session cleanup
- ✅ Session activity tracking
- ✅ IP-based session monitoring

### 4. Rate Limiting
- ✅ Login: 5 attempts per minute
- ✅ Registration: 3 attempts per minute
- ✅ General API: 100 requests per minute
- ✅ IP-based brute force protection

## 📊 **Monitoring and Logging**

### Audit Logging
```python
# Automatic audit logging for all auth events
AuditLogRepository.create(
    db, user_id, "login", "auth", 
    f"Login from IP {client_ip}", client_ip, user_agent
)
```

### Log Levels
- **INFO**: Successful operations
- **WARNING**: Authentication failures
- **ERROR**: System errors and exceptions
- **DEBUG**: Detailed debugging information

## 🚀 **Production Deployment**

### Environment Variables
```env
# Production settings
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://prod_user:prod_pass@prod_host:5432/prod_db
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Security Headers
```python
# Automatic security headers
response.headers["X-Content-Type-Options"] = "nosniff"
response.headers["X-Frame-Options"] = "DENY"
response.headers["X-XSS-Protection"] = "1; mode=block"
response.headers["Strict-Transport-Security"] = "max-age=31536000"
```

### HTTPS Configuration
```python
# Set secure=True for production cookies
response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,
    secure=True,  # HTTPS only
    samesite="lax",
    max_age=expires_in
)
```

## 🔧 **Troubleshooting**

### Common Issues

#### 1. Database Connection Errors
```bash
# Check database connectivity
python -c "from db.database import check_database_health; print(check_database_health())"
```

#### 2. Token Validation Errors
```python
# Verify token manually
from auth.auth import verify_token
payload = verify_token(token)
print(payload)
```

#### 3. Session Issues
```python
# Check active sessions
from auth.auth import session_manager
print(session_manager.get_active_sessions_count())
```

### Debug Mode
```python
# Enable debug logging
import logging
logging.getLogger('auth').setLevel(logging.DEBUG)
```

## 📚 **Additional Resources**

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [JWT Best Practices](https://auth0.com/blog/a-look-at-the-latest-draft-for-jwt-bcp/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 🤝 **Contributing**

When contributing to the authentication system:

1. **Follow SOLID Principles**
2. **Add comprehensive tests**
3. **Update documentation**
4. **Follow security best practices**
5. **Add audit logging for new features**

## 📄 **License**

This authentication system is part of the SafeRide project and follows the same licensing terms. 