import pytest
import os
import sys
from unittest.mock import patch

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock environment variables for testing
@pytest.fixture(autouse=True)
def mock_env_vars():
    """Mock environment variables for testing"""
    with patch.dict(os.environ, {
        'SECRET_KEY': 'test-secret-key-for-testing-only',
        'DATABASE_URL': 'postgresql://test:test@localhost/test_db',
        'ACCESS_TOKEN_EXPIRE_MINUTES': '30'
    }):
        yield

@pytest.fixture
def test_client():
    """Create a test client for the FastAPI app"""
    from fastapi.testclient import TestClient
    from main import app
    return TestClient(app)

@pytest.fixture
def mock_db_session():
    """Mock database session for testing"""
    with patch('db.database.get_db_session') as mock:
        yield mock

@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "id": "test-user-123",
        "email": "test@example.com",
        "password_hash": "hashed_password",
        "first_name": "Test",
        "last_name": "User",
        "phone": "+1234567890",
        "role_id": "role-1",
        "company_id": None,
        "is_active": True,
        "is_verified": True,
        "profile_picture": None,
        "last_login": None
    }

@pytest.fixture
def sample_role_data():
    """Sample role data for testing"""
    return {
        "id": "role-1",
        "name": "passenger",
        "description": "Passenger role",
        "permissions": ["view_rides", "create_rides"],
        "is_active": True
    } 