#!/usr/bin/env python3
"""
Environment Setup Script for SafeRide API

This script helps users create a proper .env file with secure defaults.
"""

import os
import secrets
import string
from pathlib import Path

def generate_secret_key(length: int = 32) -> str:
    """Generate a cryptographically secure secret key"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_env_file():
    """Create a .env file with secure defaults"""
    env_file = Path(".env")
    
    if env_file.exists():
        print("⚠️  .env file already exists. Backing up to .env.backup")
        env_file.rename(".env.backup")
    
    # Generate secure secret key
    secret_key = generate_secret_key(64)
    
    env_content = f"""# SafeRide API Environment Configuration
# Generated automatically - Review and update as needed

# Application Settings
APP_NAME=SafeRide API
APP_VERSION=1.0.0
DEBUG=true

# Security Settings
SECRET_KEY={secret_key}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Settings
DATABASE_URL=postgresql://saferide_user:saferide_password@localhost:5432/saferide_db
DB_HOST=localhost
DB_PORT=5432
DB_NAME=saferide_db
DB_USER=saferide_user
DB_PASSWORD=saferide_password

# CORS Settings
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=["*"]
CORS_ALLOW_HEADERS=["*"]

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_PER_HOUR=1000

# External APIs
WAZE_API_KEY=your-waze-api-key-here

# Server Settings
HOST=0.0.0.0
PORT=8000

# Redis Settings (for rate limiting and caching)
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=INFO
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Created .env file with secure defaults")
    print(f"🔑 Generated secure SECRET_KEY: {secret_key[:20]}...")
    print(f"📝 Please review and update the .env file as needed")

def main():
    """Main setup function"""
    print("🚀 SafeRide API Environment Setup")
    print("=" * 40)
    
    try:
        create_env_file()
        print("\n✅ Environment setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Review the .env file and update values as needed")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Run tests: python run_tests.py")
        print("4. Start the application: python main.py")
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 