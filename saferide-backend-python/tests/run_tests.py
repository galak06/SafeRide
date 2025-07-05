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

def run_specific_test(test_file):
    """Run a specific test file"""
    print(f"🧪 Running specific test: {test_file}")
    
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            f"tests/{test_file}", 
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

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test file
        test_file = sys.argv[1]
        success = run_specific_test(test_file)
    else:
        # Run all tests
        success = run_tests()
    
    sys.exit(0 if success else 1) 