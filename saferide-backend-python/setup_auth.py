#!/usr/bin/env python3
"""
Setup script for SafeRide Authentication System

This script initializes the database with:
1. Database tables
2. Roles and permissions
3. Test users

Usage:
    python setup_auth.py
"""

import os
import sys
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main setup function"""
    try:
        logger.info("🚀 Setting up SafeRide Authentication System...")
        logger.info("=" * 60)
        
        # Import after path setup
        from db.init_db import init_database_with_data
        
        # Initialize database with all data
        init_database_with_data()
        
        logger.info("=" * 60)
        logger.info("✅ Authentication system setup completed successfully!")
        logger.info("")
        logger.info("📋 Test Users Created:")
        logger.info("   Admin:     admin@saferide.com / password123")
        logger.info("   Child 1:   child1@example.com / password123")
        logger.info("   Child 2:   child2@example.com / password123")
        logger.info("   Escort:    escort@example.com / password123")
        logger.info("   Manager:   manager@example.com / password123")
        logger.info("")
        logger.info("🔐 Authentication Features:")
        logger.info("   ✅ Database user lookup")
        logger.info("   ✅ JWT access and refresh tokens")
        logger.info("   ✅ Session management")
        logger.info("   ✅ Role-based authorization")
        logger.info("   ✅ Permission-based authorization")
        logger.info("   ✅ Audit logging")
        logger.info("   ✅ Brute force protection")
        logger.info("   ✅ Token refresh functionality")
        logger.info("")
        logger.info("🌐 API Endpoints:")
        logger.info("   POST /api/auth/login     - User login")
        logger.info("   POST /api/auth/refresh   - Refresh access token")
        logger.info("   GET  /api/auth/me        - Get current user")
        logger.info("   POST /api/auth/logout    - User logout")
        logger.info("   GET  /api/auth/sessions/active    - Get active sessions (admin)")
        logger.info("   POST /api/auth/sessions/cleanup   - Clean expired sessions (admin)")
        logger.info("")
        logger.info("🧪 To run tests:")
        logger.info("   pytest tests/test_complete_auth.py -v")
        logger.info("")
        logger.info("🚀 To start the server:")
        logger.info("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        logger.info("")
        logger.info("🔗 API Documentation:")
        logger.info("   http://localhost:8000/docs")
        
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        logger.error("Make sure you're in the correct directory and all dependencies are installed.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Setup failed: {e}")
        logger.error("Check the error message above and ensure your database is properly configured.")
        sys.exit(1)

if __name__ == "__main__":
    main() 