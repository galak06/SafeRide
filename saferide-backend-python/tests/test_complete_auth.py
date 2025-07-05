import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from jose import jwt
from main import app
from db.database import get_db
from core.config import settings
from auth.auth import session_manager

# Override the database dependency for all tests
def override_get_db():
    """Override database dependency for testing"""
    mock_db = MagicMock()
    yield mock_db

# Apply the override to the app
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    """Create a fresh test client for each test"""
    test_client = TestClient(app)
    yield test_client
    # Clear cookies after each test
    test_client.cookies.clear()
    # Clear session manager
    session_manager.active_sessions.clear()

@pytest.fixture
def mock_user(mock_role):
    """Mock user for testing"""
    from auth.auth import get_password_hash
    class PatchedUser:
        def __init__(self):
            self.id = "test-user-123"
            self.email = "test@example.com"
            self.hashed_password = get_password_hash("testpassword123")
            self.first_name = "Test"
            self.last_name = "User"
            self.phone = "+1234567890"
            self.is_active = True
            self.is_verified = True
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            self.last_login = None
            self.roles = [mock_role]
    
    return PatchedUser()

@pytest.fixture
def mock_role():
    """Mock role for testing"""
    class PatchedRole:
        def __init__(self):
            self.id = "role-1"
            self.name = "passenger"
            self.description = "Passenger role"
            self.permissions = []
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
    
    return PatchedRole()

@pytest.fixture
def mock_db():
    """Mock database session"""
    return MagicMock()

class TestCompleteAuthentication:
    """Test complete authentication flow"""
    
    def test_login_with_database_lookup(self, client, mock_user, mock_role):
        """Test successful login with database user lookup"""
        with patch('db.repositories.UserRepository.get_by_email', return_value=mock_user), \
             patch('db.repositories.UserRepository.update_last_login'), \
             patch('db.repositories.AuditLogRepository.create'):
            
            response = client.post("/api/auth/login", json={
                "email": "test@example.com",
                "password": "testpassword123"
            })
            
            assert response.status_code == 200
            data = response.json()
            
            # Check response structure
            assert "access_token" in data
            assert "refresh_token" in data
            assert "token_type" in data
            assert "expires_in" in data
            assert "refresh_expires_in" in data
            assert "user" in data
            
            # Check user data
            user_data = data["user"]
            assert user_data["email"] == "test@example.com"
            assert user_data["first_name"] == "Test"
            assert user_data["last_name"] == "User"
            assert "role" in user_data
            
            # Check cookies
            cookies = response.cookies
            assert "access_token" in cookies
            assert "refresh_token" in cookies
    
    def test_token_refresh(self, client, mock_user):
        """Test token refresh functionality"""
        # First login to get tokens
        with patch('db.repositories.UserRepository.get_by_email', return_value=mock_user), \
             patch('db.repositories.UserRepository.update_last_login'), \
             patch('db.repositories.AuditLogRepository.create'):
            
            login_response = client.post("/api/auth/login", json={
                "email": "test@example.com",
                "password": "testpassword123"
            })
            
            assert login_response.status_code == 200
            login_data = login_response.json()
            refresh_token = login_data["refresh_token"]
        
        # Now test token refresh
        with patch('db.repositories.UserRepository.get_by_id', return_value=mock_user), \
             patch('db.repositories.AuditLogRepository.create'):
            
            # Set refresh token cookie
            client.cookies.set("refresh_token", refresh_token)
            
            response = client.post("/api/auth/refresh", json={})
            
            assert response.status_code == 200
            data = response.json()
            
            # Check response structure
            assert "access_token" in data
            assert "token_type" in data
            assert "expires_in" in data
            
            # Check that new access token is different
            assert data["access_token"] != login_data["access_token"]
            
            # Check that new access token cookie is set
            cookies = response.cookies
            assert "access_token" in cookies
    
    def test_get_current_user_with_database_lookup(self, client, mock_user):
        """Test getting current user info with database lookup"""
        # First login to get access token
        with patch('db.repositories.UserRepository.get_by_email', return_value=mock_user), \
             patch('db.repositories.UserRepository.update_last_login'), \
             patch('db.repositories.AuditLogRepository.create'):
            
            login_response = client.post("/api/auth/login", json={
                "email": "test@example.com",
                "password": "testpassword123"
            })
            
            assert login_response.status_code == 200
            login_data = login_response.json()
            access_token = login_data["access_token"]
        
        # Test getting current user info
        with patch('db.repositories.UserRepository.get_by_id', return_value=mock_user):
            # Set access token cookie
            client.cookies.set("access_token", access_token)
            
            response = client.get("/api/auth/me")
            
            assert response.status_code == 200
            data = response.json()
            
            # Check user data
            assert data["email"] == "test@example.com"
            assert data["first_name"] == "Test"
            assert data["last_name"] == "User"
            assert "role" in data
    
    def test_logout_with_session_invalidation(self, client, mock_user):
        """Test logout with session invalidation"""
        # First login to get access token
        with patch('db.repositories.UserRepository.get_by_email', return_value=mock_user), \
             patch('db.repositories.UserRepository.update_last_login'), \
             patch('db.repositories.AuditLogRepository.create'):
            
            login_response = client.post("/api/auth/login", json={
                "email": "test@example.com",
                "password": "testpassword123"
            })
            
            assert login_response.status_code == 200
            login_data = login_response.json()
            access_token = login_data["access_token"]
        
        # Test logout
        with patch('db.repositories.AuditLogRepository.create'):
            # Set access token cookie
            client.cookies.set("access_token", access_token)
            
            response = client.post("/api/auth/logout", json={})
            
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Logged out successfully"
            
            # Check that cookies are cleared by looking at Set-Cookie headers
            set_cookie_headers = [value for key, value in response.headers.items() if key.lower() == 'set-cookie']
            assert any('access_token' in header and ('max-age=0' in header or 'Max-Age=0' in header) for header in set_cookie_headers)
            assert any('refresh_token' in header and ('max-age=0' in header or 'Max-Age=0' in header) for header in set_cookie_headers)
    
    def test_session_management(self, client, mock_user):
        """Test session management functionality"""
        # Test session creation during login
        with patch('db.repositories.UserRepository.get_by_email', return_value=mock_user), \
             patch('db.repositories.UserRepository.update_last_login'), \
             patch('db.repositories.AuditLogRepository.create'):
            
            response = client.post("/api/auth/login", json={
                "email": "test@example.com",
                "password": "testpassword123"
            })
            
            assert response.status_code == 200
            data = response.json()
            
            # Check that session was created
            user_id = mock_user.id
            session = session_manager.get_session(user_id)
            assert session is not None
            assert session["user_id"] == user_id
            assert session["is_active"] == True
        
        # Test session invalidation during logout
        with patch('db.repositories.AuditLogRepository.create'):
            client.cookies.set("access_token", data["access_token"])
            
            response = client.post("/api/auth/logout", json={})
            
            assert response.status_code == 200
            
            # Check that session was invalidated
            session = session_manager.get_session(user_id)
            assert session is None or session["is_active"] == False
    
    def test_invalid_refresh_token(self, client):
        """Test token refresh with invalid refresh token"""
        # Set invalid refresh token cookie
        client.cookies.set("refresh_token", "invalid-token")
        
        response = client.post("/api/auth/refresh", json={})
        
        assert response.status_code == 401
        data = response.json()
        assert "Invalid refresh token" in data["detail"]
    
    def test_expired_access_token(self, client, mock_user):
        """Test access with expired access token"""
        # Create an expired access token
        expired_payload = {
            "sub": mock_user.id,
            "exp": datetime.utcnow() - timedelta(hours=1),  # Expired 1 hour ago
            "type": "access"
        }
        expired_token = jwt.encode(expired_payload, settings.secret_key, algorithm=settings.algorithm)
        
        # Set expired access token cookie
        client.cookies.set("access_token", expired_token)
        
        response = client.get("/api/auth/me")
        
        assert response.status_code == 401
        data = response.json()
        assert "Invalid token" in data["detail"]
    
    def test_invalid_token_type(self, client, mock_user):
        """Test access with wrong token type"""
        # Create a refresh token (wrong type for access endpoint)
        refresh_payload = {
            "sub": mock_user.id,
            "exp": datetime.utcnow() + timedelta(days=7),
            "type": "refresh"
        }
        refresh_token = jwt.encode(refresh_payload, settings.secret_key, algorithm=settings.algorithm)
        
        # Set refresh token as access token cookie
        client.cookies.set("access_token", refresh_token)
        
        response = client.get("/api/auth/me")
        
        assert response.status_code == 401
        data = response.json()
        assert "Invalid token type" in data["detail"]
    
    def test_user_not_found(self, client):
        """Test authentication with non-existent user"""
        # Create token for non-existent user
        payload = {
            "sub": "non-existent-user-id",
            "exp": datetime.utcnow() + timedelta(hours=1),
            "type": "access"
        }
        token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
        
        # Set token cookie
        client.cookies.set("access_token", token)
        
        with patch('db.repositories.UserRepository.get_by_id', return_value=None):
            response = client.get("/api/auth/me")
            
            assert response.status_code == 401
            data = response.json()
            assert "User not found" in data["detail"]
    
    def test_inactive_user(self, client, mock_user):
        """Test authentication with inactive user"""
        # Make user inactive
        mock_user.is_active = False
        
        # First login to get access token
        with patch('db.repositories.UserRepository.get_by_email', return_value=mock_user), \
             patch('db.repositories.UserRepository.update_last_login'), \
             patch('db.repositories.AuditLogRepository.create'):
            
            login_response = client.post("/api/auth/login", json={
                "email": "test@example.com",
                "password": "testpassword123"
            })
            
            # Should fail because user is inactive
            assert login_response.status_code == 401
            data = login_response.json()
            assert "User account is inactive" in data["detail"]
    
    def test_session_cleanup(self, client, mock_user):
        """Test session cleanup functionality"""
        # Create some sessions
        session_manager.create_session("user1", "token1", "refresh1")
        session_manager.create_session("user2", "token2", "refresh2")
        
        # Initially should have 2 active sessions
        active_count = len([s for s in session_manager.active_sessions.values() if s.get("is_active")])
        assert active_count == 2
        
        # Clean up expired sessions (not implemented in current version)
        # cleaned_count = session_manager.cleanup_expired_sessions()
        
        # Should still have 2 sessions (not expired yet)
        # assert cleaned_count == 0
        active_count = len([s for s in session_manager.active_sessions.values() if s.get("is_active")])
        assert active_count == 2
        
        # Invalidate one session
        session_manager.invalidate_session("user1")
        
        # Should have 1 active session
        active_count = len([s for s in session_manager.active_sessions.values() if s.get("is_active")])
        assert active_count == 1

class TestAuthorization:
    """Test authorization functionality"""
    
    def test_role_based_authorization(self, client, mock_user, mock_role):
        """Test role-based authorization"""
        # Set up mock user with specific role
        mock_role.name = "admin"
        mock_user.roles = [mock_role]
        
        with patch('db.repositories.UserRepository.get_by_email', return_value=mock_user), \
             patch('db.repositories.UserRepository.get_by_id', return_value=mock_user), \
             patch('db.repositories.UserRepository.update_last_login'), \
             patch('db.repositories.AuditLogRepository.create'):
            
            # Login
            login_response = client.post("/api/auth/login", json={
                "email": "test@example.com",
                "password": "testpassword123"
            })
            
            assert login_response.status_code == 200
            login_data = login_response.json()
            access_token = login_data["access_token"]
            
            # Test admin-only endpoint
            client.cookies.set("access_token", access_token)
            
            response = client.get("/api/auth/sessions/active")
            
            # Should succeed because user has admin role
            assert response.status_code == 200
            data = response.json()
            assert "active_sessions" in data
    
    def test_permission_based_authorization(self, client, mock_user, mock_role):
        """Test permission-based authorization"""
        # Set up mock user with specific permissions
        class MockPermission:
            def __init__(self, name):
                self.name = name
        
        mock_role.permissions = [MockPermission("user_read")]
        mock_user.roles = [mock_role]
        
        with patch('db.repositories.UserRepository.get_by_email', return_value=mock_user), \
             patch('db.repositories.UserRepository.get_by_id', return_value=mock_user), \
             patch('db.repositories.UserRepository.update_last_login'), \
             patch('db.repositories.AuditLogRepository.create'):
            
            # Login
            login_response = client.post("/api/auth/login", json={
                "email": "test@example.com",
                "password": "testpassword123"
            })
            
            assert login_response.status_code == 200
            login_data = login_response.json()
            access_token = login_data["access_token"]
            
            # Test permission checking
            client.cookies.set("access_token", access_token)
            
            # This would test permission-based endpoints when implemented
            # For now, we just verify the user can access basic endpoints
            response = client.get("/api/auth/me")
            assert response.status_code == 200 