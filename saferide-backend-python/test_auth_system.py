#!/usr/bin/env python3
"""
Simple authentication system test script

This script tests the basic functionality of the authentication system
without requiring the full test suite or database setup.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    
    # Set required environment variables for testing
    import os
    os.environ.setdefault('SECRET_KEY', 'test-secret-key-for-testing-only-32-chars-long')
    os.environ.setdefault('DATABASE_URL', 'postgresql://test:test@localhost:5432/saferide_test_db')
    os.environ.setdefault('GOOGLE_MAPS_API_KEY', 'test-google-maps-key')
    
    try:
        from auth.auth import (
            get_password_hash, verify_password, create_access_token, 
            create_refresh_token, verify_token, verify_refresh_token,
            session_manager
        )
        print("✅ Auth module imports successful")
        
        from services.auth_service import AuthService
        print("✅ AuthService import successful")
        
        from models.responses import LoginResponse, TokenRefreshResponse, UserResponse
        print("✅ Response models import successful")
        
        from core.config import settings
        print("✅ Config import successful")
        
        from db.repositories import UserRepository, RoleRepository, PermissionRepository
        print("✅ Repository imports successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_password_hashing():
    """Test password hashing functionality"""
    print("\n🔐 Testing password hashing...")
    
    try:
        from auth.auth import get_password_hash, verify_password
        
        # Test password hashing
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        print(f"   Original password: {password}")
        print(f"   Hashed password: {hashed[:20]}...")
        
        # Test password verification
        is_valid = verify_password(password, hashed)
        is_invalid = verify_password("wrongpassword", hashed)
        
        print(f"   Correct password verification: {is_valid}")
        print(f"   Wrong password verification: {is_invalid}")
        
        if is_valid and not is_invalid:
            print("✅ Password hashing tests passed")
            return True
        else:
            print("❌ Password hashing tests failed")
            return False
            
    except Exception as e:
        print(f"❌ Password hashing error: {e}")
        return False

def test_token_creation():
    """Test JWT token creation and verification"""
    print("\n🎫 Testing JWT token creation...")
    
    try:
        from auth.auth import create_access_token, create_refresh_token, verify_token, verify_refresh_token
        
        user_id = "test-user-123"
        
        # Create tokens
        access_token = create_access_token({"sub": user_id})
        refresh_token = create_refresh_token({"sub": user_id})
        
        print(f"   Access token: {access_token[:20]}...")
        print(f"   Refresh token: {refresh_token[:20]}...")
        
        # Verify tokens
        access_payload = verify_token(access_token)
        refresh_payload = verify_refresh_token(refresh_token)
        
        print(f"   Access token payload: {access_payload}")
        print(f"   Refresh token payload: {refresh_payload}")
        
        # Test invalid tokens
        invalid_access = verify_token("invalid-token")
        invalid_refresh = verify_refresh_token("invalid-token")
        
        print(f"   Invalid access token: {invalid_access}")
        print(f"   Invalid refresh token: {invalid_refresh}")
        
        if access_payload and refresh_payload and not invalid_access and not invalid_refresh:
            print("✅ JWT token tests passed")
            return True
        else:
            print("❌ JWT token tests failed")
            return False
            
    except Exception as e:
        print(f"❌ JWT token error: {e}")
        return False

def test_session_management():
    """Test session management functionality"""
    print("\n🔄 Testing session management...")
    
    try:
        from auth.auth import session_manager
        
        user_id = "test-user-123"
        access_token = "test-access-token"
        refresh_token = "test-refresh-token"
        
        # Create session
        session = session_manager.create_session(user_id, access_token, refresh_token)
        print(f"   Created session: {session}")
        
        # Get session
        retrieved_session = session_manager.get_session(user_id)
        print(f"   Retrieved session: {retrieved_session}")
        
        # Check active sessions count
        active_count = len([s for s in session_manager.active_sessions.values() if s.get("is_active")])
        print(f"   Active sessions count: {active_count}")
        
        # Refresh session
        new_access_token = "new-access-token"
        refreshed_session = session_manager.refresh_session(user_id, new_access_token)
        print(f"   Refreshed session: {refreshed_session}")
        
        # Invalidate session
        invalidated = session_manager.invalidate_session(user_id)
        print(f"   Session invalidated: {invalidated}")
        
        # Check session after invalidation
        invalid_session = session_manager.get_session(user_id)
        print(f"   Session after invalidation: {invalid_session}")
        
        if session and retrieved_session and active_count == 1 and refreshed_session and invalidated and not invalid_session:
            print("✅ Session management tests passed")
            return True
        else:
            print("❌ Session management tests failed")
            return False
            
    except Exception as e:
        print(f"❌ Session management error: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("\n⚙️ Testing configuration...")
    
    # Set required environment variables for testing
    import os
    os.environ.setdefault('SECRET_KEY', 'test-secret-key-for-testing-only-32-chars-long')
    os.environ.setdefault('DATABASE_URL', 'postgresql://test:test@localhost:5432/saferide_test_db')
    os.environ.setdefault('GOOGLE_MAPS_API_KEY', 'test-google-maps-key')
    
    try:
        from core.config import settings
        
        print(f"   App name: {settings.app_name}")
        print(f"   Debug mode: {settings.debug}")
        print(f"   Algorithm: {settings.algorithm}")
        print(f"   Token expire minutes: {settings.access_token_expire_minutes}")
        print(f"   CORS origins: {settings.cors_origins}")
        
        # Check required settings
        if settings.secret_key and settings.database_url:
            print("✅ Configuration tests passed")
            return True
        else:
            print("❌ Configuration tests failed - missing required settings")
            return False
            
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 SafeRide Authentication System Test")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Configuration Tests", test_configuration),
        ("Password Hashing Tests", test_password_hashing),
        ("JWT Token Tests", test_token_creation),
        ("Session Management Tests", test_session_management),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed!")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Authentication system is working correctly.")
        print("\n🚀 Next steps:")
        print("   1. Set up your database")
        print("   2. Run: python setup_auth.py")
        print("   3. Start the server: uvicorn main:app --reload")
        print("   4. Run full test suite: python tests/run_tests.py --auth")
        return True
    else:
        print("💥 Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 