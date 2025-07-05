"""
Pytest configuration for SafeRide API tests

This file contains common fixtures and configurations used across all tests.
"""

import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from datetime import datetime
from sqlalchemy.orm import Session

from main import app
from db.database import get_db
from auth.auth import session_manager, get_password_hash

# Global test configuration
pytest_plugins = []

@pytest.fixture(scope="session")
def test_app():
    """Create test application instance"""
    return app

@pytest.fixture(scope="function")
def client(test_app):
    """Create a fresh test client for each test"""
    test_client = TestClient(test_app)
    yield test_client
    # Clear cookies after each test
    test_client.cookies.clear()
    # Clear session manager
    session_manager.active_sessions.clear()

@pytest.fixture(scope="function")
def mock_db():
    """Create a mock database session"""
    return MagicMock(spec=Session)

@pytest.fixture(scope="function")
def mock_user():
    """Create a mock user for testing"""
    class MockUser:
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
            self.roles = [mock_role()]
    
    return MockUser()

@pytest.fixture(scope="function")
def mock_role():
    """Create a mock role for testing"""
    class MockRole:
        def __init__(self):
            self.id = "role-1"
            self.name = "passenger"
            self.description = "Passenger role"
            self.permissions = []
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
    
    return MockRole()

@pytest.fixture(scope="function")
def mock_admin_user():
    """Create a mock admin user for testing"""
    class MockAdminUser:
        def __init__(self):
            self.id = "admin-user-123"
            self.email = "admin@saferide.com"
            self.hashed_password = get_password_hash("password123")
            self.first_name = "Admin"
            self.last_name = "User"
            self.phone = "+1234567890"
            self.is_active = True
            self.is_verified = True
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            self.last_login = None
            self.roles = [mock_admin_role()]
    
    return MockAdminUser()

@pytest.fixture(scope="function")
def mock_admin_role():
    """Create a mock admin role for testing"""
    class MockAdminRole:
        def __init__(self):
            self.id = "admin-role-1"
            self.name = "admin"
            self.description = "Administrator role"
            self.permissions = []
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
    
    return MockAdminRole()

@pytest.fixture(scope="function")
def mock_inactive_user():
    """Create a mock inactive user for testing"""
    class MockInactiveUser:
        def __init__(self):
            self.id = "inactive-user-123"
            self.email = "inactive@example.com"
            self.hashed_password = get_password_hash("password123")
            self.first_name = "Inactive"
            self.last_name = "User"
            self.phone = "+1234567890"
            self.is_active = False  # Inactive user
            self.is_verified = True
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            self.last_login = None
            self.roles = [mock_role()]
    
    return MockInactiveUser()

@pytest.fixture(scope="function")
def mock_unverified_user():
    """Create a mock unverified user for testing"""
    class MockUnverifiedUser:
        def __init__(self):
            self.id = "unverified-user-123"
            self.email = "unverified@example.com"
            self.hashed_password = get_password_hash("password123")
            self.first_name = "Unverified"
            self.last_name = "User"
            self.phone = "+1234567890"
            self.is_active = True
            self.is_verified = False  # Unverified user
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            self.last_login = None
            self.roles = [mock_role()]
    
    return MockUnverifiedUser()

@pytest.fixture(scope="function")
def mock_permission():
    """Create a mock permission for testing"""
    class MockPermission:
        def __init__(self):
            self.id = "perm-1"
            self.name = "user_read"
            self.description = "Read user information"
            self.resource = "user"
            self.action = "read"
            self.created_at = datetime.utcnow()
    
    return MockPermission()

@pytest.fixture(scope="function")
def auth_headers():
    """Create authentication headers for testing"""
    def _auth_headers(token):
        return {"Authorization": f"Bearer {token}"}
    return _auth_headers

@pytest.fixture(scope="function")
def valid_login_data():
    """Valid login credentials for testing"""
    return {
        "email": "test@example.com",
        "password": "testpassword123"
    }

@pytest.fixture(scope="function")
def invalid_login_data():
    """Invalid login credentials for testing"""
    return {
        "email": "wrong@example.com",
        "password": "wrongpassword"
    }

@pytest.fixture(scope="function")
def malformed_login_data():
    """Malformed login data for testing"""
    return {
        "email": "invalid-email",
        "password": "short"
    }

# Override database dependency for all tests
def override_get_db():
    """Override database dependency for testing"""
    mock_db = MagicMock(spec=Session)
    yield mock_db

# Apply the override to the app
app.dependency_overrides[get_db] = override_get_db

# Test markers
pytestmark = [
    pytest.mark.asyncio,
]

# Test configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "auth: mark test as authentication test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on file names"""
    for item in items:
        # Add auth marker to authentication tests
        if "auth" in item.nodeid.lower():
            item.add_marker(pytest.mark.auth)
        
        # Add integration marker to integration tests
        if "integration" in item.nodeid.lower():
            item.add_marker(pytest.mark.integration)
        
        # Add unit marker to unit tests
        if "unit" in item.nodeid.lower():
            item.add_marker(pytest.mark.unit)

# Test utilities
class TestUtils:
    """Utility functions for tests"""
    
    @staticmethod
    def create_test_token(user_id: str, token_type: str = "access", expired: bool = False):
        """Create a test JWT token"""
        from jose import jwt
        from core.config import settings
        from datetime import datetime, timedelta
        
        payload = {
            "sub": user_id,
            "type": token_type,
            "exp": datetime.utcnow().timestamp() - 3600 if expired else (datetime.utcnow() + timedelta(hours=1)).timestamp()
        }
        
        return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    
    @staticmethod
    def assert_auth_response_structure(response_data):
        """Assert that authentication response has correct structure"""
        assert "access_token" in response_data
        assert "refresh_token" in response_data
        assert "token_type" in response_data
        assert "expires_in" in response_data
        assert "refresh_expires_in" in response_data
        assert "user" in response_data
        
        user_data = response_data["user"]
        assert "id" in user_data
        assert "email" in user_data
        assert "first_name" in user_data
        assert "last_name" in user_data
        assert "role" in user_data
    
    @staticmethod
    def assert_user_data_structure(user_data):
        """Assert that user data has correct structure"""
        assert "id" in user_data
        assert "email" in user_data
        assert "first_name" in user_data
        assert "last_name" in user_data
        assert "role" in user_data
        assert "is_active" in user_data
        assert "is_verified" in user_data 