import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from datetime import datetime
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
    from unittest.mock import MagicMock
    
    mock_user = MagicMock()
    # Configure the mock to return actual values instead of MagicMock objects
    mock_user.id = "test-user-123"
    mock_user.email = "test@example.com"
    mock_user.hashed_password = get_password_hash("testpassword123")
    mock_user.first_name = "Test"
    mock_user.last_name = "User"
    mock_user.phone = "+1234567890"
    mock_user.is_active = True
    mock_user.is_verified = True
    mock_user.created_at = datetime.utcnow()
    mock_user.updated_at = datetime.utcnow()
    mock_user.last_login = None
    mock_user.roles = [mock_role]
    
    # Configure the mock to return the actual values when accessed
    # Note: MagicMock automatically handles attribute access
    
    return mock_user

@pytest.fixture
def mock_role():
    """Mock role for testing"""
    from unittest.mock import MagicMock
    
    mock_role = MagicMock()
    mock_role.id = "role-1"
    mock_role.name = "passenger"
    mock_role.description = "Passenger role"
    mock_role.permissions = []
    mock_role.created_at = datetime.utcnow()
    mock_role.updated_at = datetime.utcnow()
    
    return mock_role

@pytest.fixture
def mock_db():
    """Mock database session"""
    return MagicMock()

class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_login_success(self, client, mock_user, mock_role):
        """Test successful login with new response structure"""
        with patch('db.repositories.UserRepository.get_by_email', return_value=mock_user), \
             patch('db.repositories.UserRepository.update_last_login'), \
             patch('db.repositories.AuditLogRepository.create'):
            
            response = client.post("/api/auth/login", json={
                "email": "test@example.com",
                "password": "testpassword123"
            })
            
            assert response.status_code == 200
            data = response.json()
            
            # Check new response structure
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
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        with patch('db.repositories.UserRepository.get_by_email', return_value=None):
            response = client.post("/api/auth/login", json={
                "email": "wrong@example.com",
                "password": "wrongpassword"
            })
            
            assert response.status_code == 401
            assert "Invalid email or password" in response.json()["detail"]
    
    def test_login_inactive_user(self, client, mock_user):
        """Test login with inactive user"""
        mock_user.is_active = False
        
        with patch('db.repositories.UserRepository.get_by_email', return_value=mock_user):
            response = client.post("/api/auth/login", json={
                "email": "test@example.com",
                "password": "testpassword123"
            })
            
            assert response.status_code == 401
            assert "User account is inactive" in response.json()["detail"]
    
    def test_login_missing_fields(self, client):
        """Test login with missing required fields"""
        response = client.post("/api/auth/login", json={
            "email": "test@example.com"
            # Missing password
        })
        
        assert response.status_code == 422
    
    def test_login_invalid_email_format(self, client):
        """Test login with invalid email format"""
        response = client.post("/api/auth/login", json={
            "email": "invalid-email",
            "password": "testpassword123"
        })
        
        assert response.status_code == 422

class TestTokenRefresh:
    """Test token refresh functionality"""
    
    def test_token_refresh_success(self, client, mock_user):
        """Test successful token refresh"""
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
        
        # Test token refresh
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
    
    def test_token_refresh_invalid_token(self, client):
        """Test token refresh with invalid refresh token"""
        # Set invalid refresh token cookie
        client.cookies.set("refresh_token", "invalid-token")
        
        response = client.post("/api/auth/refresh", json={})
        
        assert response.status_code == 401
        assert "Invalid refresh token" in response.json()["detail"]
    
    def test_token_refresh_no_token(self, client):
        """Test token refresh without refresh token"""
        response = client.post("/api/auth/refresh", json={})
        
        assert response.status_code == 401
        assert "Refresh token not found" in response.json()["detail"]

class TestUserInfo:
    """Test user information endpoints"""
    
    def test_get_current_user_info_authenticated(self, client, mock_user):
        """Test getting current user info with valid session (cookie)"""
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
    
    def test_get_current_user_info_no_token(self, client):
        """Test getting current user info without token"""
        response = client.get("/api/auth/me")
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]
    
    def test_get_current_user_info_invalid_token(self, client):
        """Test getting current user info with invalid token"""
        # Set invalid access token cookie
        client.cookies.set("access_token", "invalid-token")
        
        response = client.get("/api/auth/me")
        assert response.status_code == 401
        assert "Invalid token" in response.json()["detail"]
    
    def test_get_current_user_info_expired_token(self, client, mock_user):
        """Test getting current user info with expired token"""
        # Create an expired access token
        expired_payload = {
            "sub": mock_user.id,
            "exp": datetime.utcnow().timestamp() - 3600,  # Expired 1 hour ago
            "type": "access"
        }
        expired_token = jwt.encode(expired_payload, settings.secret_key, algorithm=settings.algorithm)
        
        # Set expired access token cookie
        client.cookies.set("access_token", expired_token)
        
        response = client.get("/api/auth/me")
        
        assert response.status_code == 401
        assert "Invalid token" in response.json()["detail"]

class TestLogout:
    """Test logout functionality"""
    
    def test_logout_success(self, client, mock_user):
        """Test successful logout"""
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
    
    def test_logout_without_token(self, client):
        """Test logout without access token"""
        response = client.post("/api/auth/logout", json={})
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Logged out successfully"

class TestSessionManagement:
    """Test session management functionality"""
    
    def test_session_creation_during_login(self, client, mock_user):
        """Test that session is created during login"""
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
    
    def test_session_invalidation_during_logout(self, client, mock_user):
        """Test that session is invalidated during logout"""
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
            
            # Check that session was invalidated
            user_id = mock_user.id
            session = session_manager.get_session(user_id)
            assert session is None or session["is_active"] == False

class TestAuthorization:
    """Test authorization functionality"""
    
    def test_admin_session_endpoint(self, client, mock_user):
        """Test admin-only session endpoint"""
        # Create admin user
        mock_user.roles[0].name = "admin"
    
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
    
        # Test admin endpoint with proper mocking
        with patch('db.repositories.UserRepository.get_by_id', return_value=mock_user), \
             patch('auth.auth._convert_db_user_to_model') as mock_convert:
            
            # Create a simple mock user model
            from unittest.mock import MagicMock
            mock_user_model = MagicMock()
            mock_user_model.id = "test-user-123"
            mock_user_model.is_active = True
            mock_convert.return_value = mock_user_model
            
            client.cookies.set("access_token", access_token)
            response = client.get("/api/auth/sessions/active")
    
            # Should succeed because user has admin role
            assert response.status_code == 200
            data = response.json()
            assert "active_sessions" in data
            assert "timestamp" in data
    
    def test_non_admin_session_endpoint(self, client, mock_user):
        """Test session endpoint with non-admin user"""
        # Create non-admin user (passenger)
        mock_user.roles[0].name = "passenger"
        
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
        
        # Test admin endpoint with proper mocking
        with patch('db.repositories.UserRepository.get_by_id', return_value=mock_user), \
             patch('auth.auth._convert_db_user_to_model') as mock_convert:
            
            # Create a simple mock user model
            from unittest.mock import MagicMock
            mock_user_model = MagicMock()
            mock_user_model.id = "test-user-123"
            mock_user_model.is_active = True
            mock_convert.return_value = mock_user_model
            
            client.cookies.set("access_token", access_token)
            response = client.get("/api/auth/sessions/active")
        
            # Should fail because user doesn't have admin role
            assert response.status_code == 403
            assert "Admin access required" in response.json()["detail"] 