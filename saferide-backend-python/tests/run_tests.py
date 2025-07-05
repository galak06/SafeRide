#!/usr/bin/env python3
"""
Test runner for SafeRide API

This script runs the test suite and provides detailed output.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_tests():
    """Run the test suite"""
    print("🚀 Running SafeRide API Test Suite")
    print("=" * 50)
    
    # Change to the backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Install test dependencies if needed
    print("📦 Installing test dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    
    # Run tests with coverage
    print("\n🧪 Running tests...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "-v", 
            "--tb=short",
            "--color=yes"
        ], check=False)
        
        if result.returncode == 0:
            print("\n✅ All tests passed!")
            return True
        else:
            print(f"\n❌ Tests failed with exit code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def run_authentication_tests():
    """Run authentication-specific tests"""
    print("🔐 Running Authentication Tests")
    print("=" * 40)
    
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    auth_test_files = [
        "test_auth.py",
        "test_complete_auth.py"
    ]
    
    all_passed = True
    
    for test_file in auth_test_files:
        print(f"\n📋 Running {test_file}...")
        try:
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                test_file, 
                "-v", 
                "--tb=short",
                "--color=yes"
            ], check=False)
            
            if result.returncode == 0:
                print(f"✅ {test_file} passed!")
            else:
                print(f"❌ {test_file} failed!")
                all_passed = False
                
        except Exception as e:
            print(f"❌ Error running {test_file}: {e}")
            all_passed = False
    
    return all_passed

def run_specific_test(test_file):
    """Run a specific test file"""
    print(f"🧪 Running specific test: {test_file}")
    
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            test_file, 
            "-v", 
            "--tb=short",
            "--color=yes"
        ], check=False)
        
        if result.returncode == 0:
            print(f"\n✅ Test {test_file} passed!")
            return True
        else:
            print(f"\n❌ Test {test_file} failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error running test {test_file}: {e}")
        return False

def run_test_with_coverage():
    """Run tests with coverage report"""
    print("📊 Running tests with coverage report")
    print("=" * 45)
    
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "--cov=.",
            "--cov-report=term-missing",
            "--cov-report=html",
            "-v",
            "--tb=short",
            "--color=yes"
        ], check=False)
        
        if result.returncode == 0:
            print("\n✅ Tests completed with coverage report!")
            print("📁 HTML coverage report generated in htmlcov/")
            return True
        else:
            print(f"\n❌ Tests failed with exit code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error running tests with coverage: {e}")
        return False

def show_test_categories():
    """Show available test categories"""
    print("📋 Available Test Categories")
    print("=" * 30)
    print("1. All Tests: python run_tests.py")
    print("2. Authentication Tests: python run_tests.py --auth")
    print("3. Coverage Report: python run_tests.py --coverage")
    print("4. Specific Test: python run_tests.py <test_file>")
    print("\n📁 Test Files:")
    
    backend_dir = Path(__file__).parent
    test_files = list(backend_dir.glob("test_*.py"))
    
    for test_file in test_files:
        print(f"   - {test_file.name}")
    
    print("\n🔐 Authentication Tests:")
    print("   - test_auth.py (Basic authentication)")
    print("   - test_complete_auth.py (Complete auth system)")
    
    print("\n🛡️ Security Tests:")
    print("   - test_security_fixes.py (Security features)")
    
    print("\n🚗 Service Tests:")
    print("   - test_waze_service.py (Waze integration)")
    print("   - test_ride_service.py (Ride management)")
    print("   - test_admin_service.py (Admin functionality)")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == "--auth":
            # Run authentication tests
            success = run_authentication_tests()
        elif arg == "--coverage":
            # Run tests with coverage
            success = run_test_with_coverage()
        elif arg == "--help" or arg == "-h":
            # Show help
            show_test_categories()
            sys.exit(0)
        else:
            # Run specific test file
            success = run_specific_test(arg)
    else:
        # Run all tests
        success = run_tests()
    
    if success:
        print("\n🎉 Test execution completed successfully!")
    else:
        print("\n💥 Test execution failed!")
    
    sys.exit(0 if success else 1) 