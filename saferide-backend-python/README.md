# SafeRide Backend API

A comprehensive ride-sharing application backend built with FastAPI, PostgreSQL, and modern security practices.

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL 14+
- Node.js 16+ (for frontend)

### 1. Database Setup

#### Install PostgreSQL (macOS)
```bash
# Install PostgreSQL using Homebrew
brew install postgresql@14

# Start PostgreSQL service
brew services start postgresql@14

# Create the database
createdb saferide_db
```

#### Database Initialization
```bash
# Navigate to backend directory
cd saferide-backend-python

# Initialize database tables
python -c "from db.database import init_database; init_database()"
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd saferide-backend-python

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment configuration
cp env.example .env

# Update database URL in .env file
# DATABASE_URL=postgresql://your_username@localhost:5432/saferide_db

# Start the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd saferide-frontend

# Install dependencies
npm install

# Start the frontend server
npm run dev
```

## 🧪 Test Users

The following test users are pre-configured in the database:

| Email | Password | Role | Description |
|-------|----------|------|-------------|
| `admin@saferide.com` | `password123` | Admin | Administrator user |
| `child1@example.com` | `password123` | Child | Test child user 1 |
| `child2@example.com` | `password123` | Child | Test child user 2 |
| `escort@example.com` | `password123` | Escort | Test escort user |

## 📁 Project Structure

```
saferide-backend-python/
├── auth/                    # Authentication modules
├── core/                    # Core configuration and exceptions
├── db/                      # Database models and connection
├── models/                  # Pydantic models
│   ├── base/               # Base models
│   ├── entities/           # Entity models
│   ├── requests/           # Request models
│   └── responses/          # Response models
├── routes/                 # API route handlers
├── services/               # Business logic services
├── tests/                  # Test suite
└── main.py                 # FastAPI application entry point
```

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user info

### Users
- `GET /api/users/{user_id}` - Get user by ID
- `GET /api/users/{user_id}/relationships` - Get user relationships

### Relationships
- `POST /api/relationships/` - Create relationship
- `GET /api/relationships/{relationship_id}` - Get relationship
- `PUT /api/relationships/{relationship_id}` - Update relationship
- `DELETE /api/relationships/{relationship_id}` - Delete relationship

### Rides
- `POST /api/rides` - Create ride
- `POST /api/rides/{ride_id}/confirm` - Confirm ride
- `GET /api/rides/{ride_id}` - Get ride status

### Routes
- `POST /api/route` - Calculate route
- `GET /api/traffic/{area}` - Get traffic alerts

## 🛡️ Security Features

- **JWT Authentication** - Secure token-based authentication (now via HTTP-only cookies)
- **Password Hashing** - bcrypt password hashing
- **Rate Limiting** - Brute force protection
- **Input Validation** - Comprehensive request validation
- **CORS Protection** - Cross-origin resource sharing configuration
- **Security Headers** - HTTP security headers
- **Audit Logging** - Comprehensive activity logging

> **Production Note:**
> - When setting cookies for authentication, always use `secure=True` in production so cookies are only sent over HTTPS.
> - Make sure your deployment uses HTTPS for all API and frontend traffic. Never transmit authentication cookies or credentials over plain HTTP.
> - Example (FastAPI):
>   ```python
>   response.set_cookie(
>       key="access_token",
>       value=token,
>       httponly=True,
>       secure=True,  # Set to True in production
>       samesite="lax",
>       max_age=expires_in
>   )
>   ```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_auth.py
```

## 📊 Database Schema

The application uses PostgreSQL with the following main tables:

- **users** - User accounts and profiles
- **roles** - User roles and permissions
- **permissions** - System permissions
- **driver_companies** - Driver company information
- **service_areas** - Geographic service areas
- **user_locations** - Real-time user location tracking
- **rides** - Ride records and status
- **route_plans** - Route planning and optimization
- **audit_logs** - System audit and activity logs

## 🔄 Development Workflow

1. **Start PostgreSQL**: `brew services start postgresql@14`
2. **Start Backend**: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
3. **Start Frontend**: `npm run dev`
4. **Access Application**: http://localhost:3000

## 🚀 Deployment

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/saferide_db

# Security
SECRET_KEY=your-super-secret-key-at-least-32-characters-long

# Application
DEBUG=False
APP_NAME=SafeRide API
APP_VERSION=1.0.0

# JWT
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000"]
CORS_ALLOW_CREDENTIALS=True
```

### Production Considerations

- Use environment-specific secret management
- Enable SSL/TLS for database connections
- Configure proper CORS origins
- Set up monitoring and logging
- Use connection pooling for database
- Implement proper backup strategies

## 📝 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

1. Follow the established code structure
2. Write tests for new features
3. Update documentation
4. Follow security best practices
5. Use type hints and proper error handling

## 📄 License

This project is licensed under the MIT License. 