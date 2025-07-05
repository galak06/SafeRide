# SafeRide Database Setup Guide

This guide will help you set up PostgreSQL database for the SafeRide application.

## Prerequisites

- Python 3.9+ with virtual environment
- PostgreSQL 12+ (will be installed automatically if not present)

## Quick Setup (Recommended)

### 1. Run the Setup Script

```bash
# Make sure you're in the saferide-backend-python directory
cd saferide-backend-python

# Run the PostgreSQL setup script
./setup_postgres.sh
```

This script will:
- Install PostgreSQL if not present
- Create the database and user
- Test the connection

### 2. Configure Environment Variables

```bash
# Copy the example environment file
cp env.example .env
```

The `.env` file contains:
```env
# Database Configuration
DATABASE_URL=postgresql://saferide_user:saferide_password@localhost:5432/saferide_db

# PostgreSQL Database Settings
DB_HOST=localhost
DB_PORT=5432
DB_NAME=saferide_db
DB_USER=saferide_user
DB_PASSWORD=saferide_password
```

### 3. Initialize the Database

```bash
# Activate virtual environment
source venv/bin/activate

# Initialize database with tables and initial data
python init_db.py
```

This will create:
- All database tables
- Initial permissions and roles
- Admin user (admin@saferide.com / admin123)

### 4. Start the Application

```bash
# Start the backend server
python main.py
```

## Manual Setup (Alternative)

If the automatic setup doesn't work, you can set up PostgreSQL manually:

### 1. Install PostgreSQL

**macOS (using Homebrew):**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**CentOS/RHEL:**
```bash
sudo yum install postgresql postgresql-server
sudo postgresql-setup initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 2. Create Database and User

```bash
# Connect to PostgreSQL as postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE saferide_db;
CREATE USER saferide_user WITH PASSWORD 'saferide_password';
GRANT ALL PRIVILEGES ON DATABASE saferide_db TO saferide_user;
ALTER USER saferide_user CREATEDB;
\q
```

### 3. Test Connection

```bash
# Test the connection
psql -U saferide_user -h localhost -d saferide_db -c "SELECT 1;"
```

## Database Schema

The application creates the following tables:

- **users** - User accounts and profiles
- **roles** - User roles (admin, manager, driver, passenger)
- **permissions** - System permissions
- **user_roles** - Many-to-many relationship between users and roles
- **role_permissions** - Many-to-many relationship between roles and permissions
- **driver_companies** - Driver company information
- **service_areas** - Geographic service areas for companies
- **user_locations** - User location tracking
- **rides** - Ride information and status
- **route_plans** - Route planning and optimization
- **route_stops** - Individual stops in routes
- **audit_logs** - System audit trail

## Default Credentials

After initialization, you can log in with:

- **Email:** admin@saferide.com
- **Password:** admin123

## Troubleshooting

### Connection Issues

1. **Check if PostgreSQL is running:**
   ```bash
   # macOS
   brew services list | grep postgresql
   
   # Linux
   sudo systemctl status postgresql
   ```

2. **Check connection parameters:**
   ```bash
   psql -U saferide_user -h localhost -d saferide_db
   ```

3. **Verify environment variables:**
   ```bash
   cat .env | grep DB_
   ```

### Permission Issues

If you get permission errors:

1. **Check PostgreSQL authentication:**
   ```bash
   sudo -u postgres psql -c "SELECT usename, usesysid FROM pg_user;"
   ```

2. **Update pg_hba.conf if needed:**
   ```bash
   # Find the file location
   sudo -u postgres psql -c "SHOW config_file;"
   ```

### Database Reset

To reset the database:

```bash
# Drop and recreate database
sudo -u postgres psql -c "DROP DATABASE IF EXISTS saferide_db;"
sudo -u postgres psql -c "CREATE DATABASE saferide_db;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE saferide_db TO saferide_user;"

# Reinitialize
python init_db.py
```

## Production Considerations

For production deployment:

1. **Use strong passwords** in the `.env` file
2. **Enable SSL** for database connections
3. **Configure connection pooling**
4. **Set up database backups**
5. **Use environment-specific configurations**

## Support

If you encounter issues:

1. Check the logs: `python main.py` (with DEBUG=true)
2. Verify database connection: `python -c "from database import engine; print(engine.execute('SELECT 1').scalar())"`
3. Check PostgreSQL logs: `/var/log/postgresql/` (Linux) or `brew services log postgresql` (macOS) 

## 🔍 **Comprehensive Review: High Priority Fixes Implementation**

### ✅ **SUCCESSFULLY IMPLEMENTED**

## 1. **Security Fixes - EXCELLENT** 🛡️

### ✅ Hardcoded Secret Key Resolution
- **Fixed:** Moved from hardcoded `"your-secret-key-here-change-in-production"` to environment variables
- **Implementation:** Using `pydantic-settings` with proper validation
- **Security:** Runtime validation ensures SECRET_KEY is set before app starts
- **Best Practice:** Follows 12-factor app methodology

### ✅ Rate Limiting Implementation
- **Fixed:** Added comprehensive rate limiting with `slowapi`
- **Configuration:** Configurable per-minute (100) and per-hour (1000) limits
- **Applied:** All endpoints protected with appropriate limits
- **Security:** Prevents API abuse and DDoS attacks

## 2. **Code Organization - OUTSTANDING** 🏗️

### ✅ Modular Architecture
```
saferide-backend-python/
├── core/           # Core functionality
├── routes/         # API endpoints
├── services/       # Business logic
├── tests/          # Test suite
└── main.py         # Entry point
```

### ✅ SOLID Principles Adherence
- **Single Responsibility:** Each module has clear, focused purpose
- **Open/Closed:** Services are extensible without modification
- **Dependency Inversion:** Configuration injected, not hardcoded
- **Interface Segregation:** Clean, focused service interfaces

## 3. **Error Handling - ROBUST** 🛠️

### ✅ Centralized Exception Management
- **Custom Exceptions:** `SafeRideException` hierarchy with specific error types
- **Global Handler:** Catches all unhandled exceptions
- **Standardized Responses:** Consistent error format across API
- **Logging:** Proper error logging with context

### ✅ Error Types Implemented
```python
AuthenticationError    # 401 - Auth failures
AuthorizationError     # 403 - Permission issues  
ValidationError        # 422 - Data validation
NotFoundError          # 404 - Resource not found
DatabaseError          # 500 - Database issues
```

## 4. **Testing Framework - COMPREHENSIVE** 🧪

### ✅ Test Structure
- **Unit Tests:** Individual component testing
- **Integration Tests:** API endpoint testing
- **Mock Services:** Isolated testing environment
- **Test Runner:** Automated test execution script

### ✅ Test Coverage
- Authentication endpoints
- Error handling scenarios
- Configuration validation
- Service layer testing

## 5. **Configuration Management - ENTERPRISE-GRADE** ⚙️

### ✅ Environment-Based Configuration
- **Pydantic Settings:** Type-safe configuration with validation
- **Environment Variables:** All sensitive data externalized
- **Validation:** Runtime checks for required settings
- **Flexibility:** Easy environment switching

## 6. **Security Enhancements - PRODUCTION-READY** 🔒

### ✅ CORS Configuration
- **Proper Setup:** Configurable origins, methods, headers
- **Security:** Credentials handling configured
- **Flexibility:** Environment-based configuration

### ✅ Trusted Host Middleware
- **Host Validation:** Prevents host header attacks
- **Production Ready:** Includes production domain

### ✅ Security Headers & Middleware
- **Rate Limiting:** Applied to all endpoints
- **Exception Handling:** Prevents information leakage
- **Logging:** Audit trail for security events

---

## ⚠️ **CRITICAL ISSUES IDENTIFIED**

### 1. **Type Safety Issues** 🚨
```python
<code_block_to_apply_changes_from>
```
**Problem:** The settings instantiation happens at module import time, causing startup failures.

**Fix Required:**
