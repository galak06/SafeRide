#!/usr/bin/env python3
"""
SafeRide API Startup Script

This script handles dependency installation, environment setup, and application startup.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'fastapi', 'uvicorn', 'python-jose', 'passlib', 
        'python-multipart', 'python-dotenv', 'slowapi',
        'pydantic-settings', 'pytest'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies():
    """Install missing dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_environment():
    """Set up environment if .env file doesn't exist"""
    if not Path(".env").exists():
        print("🔧 Setting up environment...")
        try:
            subprocess.run([sys.executable, "setup_env.py"], check=True)
            print("✅ Environment setup completed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to setup environment: {e}")
            return False
    else:
        print("✅ Environment file already exists")
        return True

def run_tests():
    """Run the test suite"""
    print("🧪 Running tests...")
    try:
        result = subprocess.run([
            sys.executable, "run_tests.py"
        ], check=False)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("⚠️  Some tests failed, but continuing...")
            return True  # Continue anyway for development
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def start_application():
    """Start the FastAPI application"""
    print("🚀 Starting SafeRide API...")
    try:
        subprocess.run([
            sys.executable, "main.py"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

def main():
    """Main startup function"""
    print("🚀 SafeRide API Startup")
    print("=" * 30)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ Error: main.py not found. Please run this script from the saferide-backend-python directory.")
        return False
    
    # Check and install dependencies
    missing_packages = check_dependencies()
    if missing_packages:
        print(f"📦 Missing packages: {', '.join(missing_packages)}")
        if not install_dependencies():
            return False
    else:
        print("✅ All dependencies are installed")
    
    # Setup environment
    if not setup_environment():
        return False
    
    # Run tests (optional)
    if len(sys.argv) > 1 and sys.argv[1] == "--skip-tests":
        print("⏭️  Skipping tests as requested")
    else:
        if not run_tests():
            print("⚠️  Test failures detected, but continuing...")
    
    # Start application
    start_application()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 