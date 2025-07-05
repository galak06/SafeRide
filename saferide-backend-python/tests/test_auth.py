import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
from models.base import UserModel, RoleModel
from auth import get_password_hash, create_access_token
from datetime import datetime
from db.database import get_db

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

@pytest.fixture
def mock_user():
    """Mock user for testing"""
    from auth import get_password_hash
    class PatchedUser(UserModel):
        @property
        def hashed_password(self):
            return self.password_hash
        @property
        def roles(self):
            return getattr(self, '_roles', [])
    return PatchedUser(
        id="test-user-123",
        email="test@example.com",
        password_hash=get_password_hash("testpassword123"),
        first_name="Test",
        last_name="User",
        phone="+1234567890",
        role_id="role-1",
        company_id=None,
        is_active=True,
        is_verified=True,
        profile_picture=None,
        last_login=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        parent_ids=[],
        child_ids=[],
        escort_ids=[],
        is_child=False,
        is_parent=False,
        is_escort=False
    )

@pytest.fixture
def mock_role():
    """Mock role for testing"""
    return RoleModel(
        id="role-1",
        name="passenger",
        description="Passenger role",
        permissions=["read_rides", "create_rides"],
        is_active=True
    )

@pytest.fixture
def mock_db():
    """Mock database session"""
    return MagicMock()

class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_login_success(self, client, mock_user, mock_role):
        """Test successful login"""
        # Patch roles property to return [mock_role]
        mock_user._roles = [mock_role]
        with patch('db.repositories.UserRepository.get_by_email', return_value=mock_user), \
             patch('db.repositories.RoleRepository.get_by_id', return_value=mock_role), \
             patch('db.repositories.UserRepository.update_last_login'):
            response = client.post("/api/auth/login", json={
                "email": "test@example.com",
                "password": "testpassword123"
            })
            assert response.status_code == 200
            data = response.json()
            assert data["email"] == "test@example.com"
            assert data["first_name"] == "Test"
            assert data["last_name"] == "User"
            assert "role" in data
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        with patch('db.repositories.UserRepository.get_by_email', return_value=None):
            response = client.post("/api/auth/login", json={
                "email": "wrong@example.com",
                "password": "wrongpassword"
            })
            
            assert response.status_code == 401
            assert "Invalid email or password" in response.json()["error"]["message"]
    
    def test_login_inactive_user(self, client, mock_user):
        """Test login with inactive user"""
        mock_user.is_active = False
        
        with patch('db.repositories.UserRepository.get_by_email', return_value=mock_user):
            response = client.post("/api/auth/login", json={
                "email": "test@example.com",
                "password": "testpassword123"
            })
            
            assert response.status_code == 401
            assert "User account is inactive" in response.json()["error"]["message"]
    
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

class TestUserInfo:
    """Test user information endpoints"""
    
    def test_get_current_user_info_authenticated(self, client, mock_user, mock_role):
        """Test getting current user info with valid session (cookie)"""
        # Patch roles property to return [mock_role]
        mock_user._roles = [mock_role]
        with patch('db.repositories.UserRepository.get_by_email', return_value=mock_user), \
             patch('db.repositories.UserRepository.get_by_id', return_value=mock_user), \
             patch('db.repositories.RoleRepository.get_by_id', return_value=mock_role), \
             patch('db.repositories.UserRepository.update_last_login'):
            # Login to set cookie
            login_response = client.post("/api/auth/login", json={
                "email": "test@example.com",
                "password": "testpassword123"
            })
            assert login_response.status_code == 200
            # Now call /me with the same client (cookie sent automatically)
            me_response = client.get("/api/auth/me")
            assert me_response.status_code == 200
            data = me_response.json()
            assert data["email"] == "test@example.com"
            assert data["first_name"] == "Test"
            assert data["last_name"] == "User"
            assert "role" in data
    
    def test_get_current_user_info_no_token(self, client):
        """Test getting current user info without token"""
        response = client.get("/api/auth/me")
        assert response.status_code == 401
    
    def test_get_current_user_info_invalid_token(self, client):
        """Test getting current user info with invalid token"""
        response = client.get("/api/auth/me", headers={"Authorization": "Bearer invalid-token"})
        assert response.status_code == 401 