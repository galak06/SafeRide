#!/usr/bin/env python3
"""
Test script to verify critical security fixes are working
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def test_environment_variables():
    """Test that required environment variables are properly validated"""
    print("🔍 Testing environment variable validation...")
    
    try:
        # Test that validation works when variables are present (current state)
        from core.config import settings
        
        if hasattr(settings, 'secret_key') and hasattr(settings, 'database_url'):
            if settings.secret_key and settings.database_url:
                print("✅ Environment variables are properly configured")
                
                # Test that secret key is strong enough
                if len(settings.secret_key) >= 32:
                    print("✅ Secret key meets minimum strength requirements")
                else:
                    print("⚠️  Secret key is too short (should be at least 32 characters)")
                
                return True
            else:
                print("❌ Environment variables are empty")
                return False
        else:
            print("❌ Environment variables are missing")
            return False
            
    except Exception as e:
        print(f"❌ Error testing environment variables: {e}")
        return False

def test_security_middleware():
    """Test that security middleware is properly configured"""
    print("🔍 Testing security middleware...")
    
    try:
        # Test middleware imports
        from core.middleware import (
            SecurityMiddleware, RateLimitMiddleware, SecurityHeadersMiddleware,
            InputValidationMiddleware, brute_force_protection
        )
        
        # Test brute force protection
        test_ip = "192.168.1.100"
        
        # Should not be locked initially
        if brute_force_protection.is_ip_locked(test_ip):
            print("❌ IP should not be locked initially")
            return False
        
        # Record failed attempts
        for i in range(5):
            brute_force_protection.record_failed_attempt(test_ip)
        
        # Should be locked after 5 attempts
        if not brute_force_protection.is_ip_locked(test_ip):
            print("❌ IP should be locked after 5 failed attempts")
            return False
        
        # Test successful attempt clears lockout
        brute_force_protection.record_successful_attempt(test_ip)
        if brute_force_protection.is_ip_locked(test_ip):
            print("❌ IP should not be locked after successful attempt")
            return False
        
        print("✅ Security middleware working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Error testing security middleware: {e}")
        return False

def test_input_validation():
    """Test input validation functions"""
    print("🔍 Testing input validation...")
    
    try:
        from core.middleware import SecurityMiddleware
        
        # Test email validation
        valid_emails = ["test@example.com", "user.name@domain.co.uk"]
        invalid_emails = ["invalid-email", "test@", "@domain.com", ""]
        
        for email in valid_emails:
            if not SecurityMiddleware.validate_email(email):
                print(f"❌ Valid email rejected: {email}")
                return False
        
        for email in invalid_emails:
            if SecurityMiddleware.validate_email(email):
                print(f"❌ Invalid email accepted: {email}")
                return False
        
        # Test password strength validation
        strong_passwords = ["SecurePass123!", "MyP@ssw0rd", "Str0ng#Pass"]
        weak_passwords = ["weak", "password", "123456", "onlylowercase", "ONLYUPPERCASE"]
        
        for password in strong_passwords:
            if not SecurityMiddleware.validate_password_strength(password):
                print(f"❌ Strong password rejected: {password}")
                return False
        
        for password in weak_passwords:
            if SecurityMiddleware.validate_password_strength(password):
                print(f"❌ Weak password accepted: {password}")
                return False
        
        print("✅ Input validation working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Error testing input validation: {e}")
        return False

def test_database_health():
    """Test database health check functionality"""
    print("🔍 Testing database health check...")
    
    try:
        from database import check_database_health
        
        # Test health check function exists and returns expected structure
        health = check_database_health()
        
        required_keys = ["status", "timestamp"]
        for key in required_keys:
            if key not in health:
                print(f"❌ Health check missing required key: {key}")
                return False
        
        print("✅ Database health check working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Error testing database health check: {e}")
        return False

def test_configuration():
    """Test configuration management"""
    print("🔍 Testing configuration management...")
    
    try:
        from core.config import settings, get_settings
        
        # Test that settings are properly loaded
        if not hasattr(settings, 'secret_key'):
            print("❌ Settings missing secret_key")
            return False
        
        if not hasattr(settings, 'database_url'):
            print("❌ Settings missing database_url")
            return False
        
        # Test singleton pattern
        settings1 = get_settings()
        settings2 = get_settings()
        if settings1 is not settings2:
            print("❌ Settings singleton pattern not working")
            return False
        
        print("✅ Configuration management working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Error testing configuration: {e}")
        return False

def main():
    """Run all security tests"""
    print("🚀 Running Security Fixes Verification Tests")
    print("=" * 50)
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Security Middleware", test_security_middleware),
        ("Input Validation", test_input_validation),
        ("Database Health", test_database_health),
        ("Configuration", test_configuration),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All critical security fixes are working correctly!")
        return 0
    else:
        print("⚠️  Some security fixes need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 