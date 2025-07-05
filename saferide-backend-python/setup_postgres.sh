#!/bin/bash

# SafeRide PostgreSQL Setup Script
# This script helps set up PostgreSQL for the SafeRide application

echo "🚀 Setting up PostgreSQL for SafeRide..."
echo "========================================"

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL is not installed."
    echo "📦 Installing PostgreSQL..."
    
    # Detect OS and install PostgreSQL
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install postgresql@14
            brew services start postgresql@14
        else
            echo "❌ Homebrew is required to install PostgreSQL on macOS"
            echo "Please install Homebrew first: https://brew.sh/"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y postgresql postgresql-contrib
            sudo systemctl start postgresql
            sudo systemctl enable postgresql
        elif command -v yum &> /dev/null; then
            sudo yum install -y postgresql postgresql-server
            sudo postgresql-setup initdb
            sudo systemctl start postgresql
            sudo systemctl enable postgresql
        else
            echo "❌ Unsupported Linux distribution"
            exit 1
        fi
    else
        echo "❌ Unsupported operating system"
        exit 1
    fi
else
    echo "✅ PostgreSQL is already installed"
fi

# Create database and user
echo "🗄️  Creating database and user..."

# Get PostgreSQL connection details
PSQL_USER="postgres"
PSQL_HOST="localhost"
PSQL_PORT="5432"

# Try to connect as postgres user
if psql -U $PSQL_USER -h $PSQL_HOST -p $PSQL_PORT -c "SELECT 1;" &> /dev/null; then
    echo "✅ Connected to PostgreSQL as postgres user"
else
    echo "⚠️  Could not connect as postgres user"
    echo "Please run the following commands manually:"
    echo ""
    echo "1. Switch to postgres user:"
    echo "   sudo -u postgres psql"
    echo ""
    echo "2. Create database and user:"
    echo "   CREATE DATABASE saferide_db;"
    echo "   CREATE USER saferide_user WITH PASSWORD 'saferide_password';"
    echo "   GRANT ALL PRIVILEGES ON DATABASE saferide_db TO saferide_user;"
    echo "   ALTER USER saferide_user CREATEDB;"
    echo "   \\q"
    echo ""
    echo "3. Then run this script again"
    exit 1
fi

# Create database and user
psql -U $PSQL_USER -h $PSQL_HOST -p $PSQL_PORT << EOF
CREATE DATABASE saferide_db;
CREATE USER saferide_user WITH PASSWORD 'saferide_password';
GRANT ALL PRIVILEGES ON DATABASE saferide_db TO saferide_user;
ALTER USER saferide_user CREATEDB;
\q
EOF

if [ $? -eq 0 ]; then
    echo "✅ Database and user created successfully"
else
    echo "❌ Failed to create database and user"
    exit 1
fi

# Test connection
echo "🔍 Testing database connection..."
if psql -U saferide_user -h $PSQL_HOST -p $PSQL_PORT -d saferide_db -c "SELECT 1;" &> /dev/null; then
    echo "✅ Database connection successful"
else
    echo "❌ Database connection failed"
    exit 1
fi

echo ""
echo "🎉 PostgreSQL setup completed successfully!"
echo ""
echo "📋 Database Details:"
echo "   Host: localhost"
echo "   Port: 5432"
echo "   Database: saferide_db"
echo "   User: saferide_user"
echo "   Password: saferide_password"
echo ""
echo "🔗 Next steps:"
echo "   1. Copy env.example to .env"
echo "   2. Run: python init_db.py"
echo "   3. Run: python main.py"
echo "" 