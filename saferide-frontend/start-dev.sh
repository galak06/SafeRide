#!/bin/bash

# SafeRide Development Startup Script
# This script starts both the Python backend and React frontend

echo "🚗 Starting SafeRide Development Environment..."

# Function to cleanup background processes
cleanup() {
    echo "🛑 Shutting down SafeRide..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js"
    exit 1
fi

# Start Python Backend
echo "🐍 Starting Python Backend..."
cd saferide-backend-python

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating environment file..."
    cp env.example .env
fi

# Start backend server
echo "🚀 Starting backend server on http://localhost:8000"
python main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if ! curl -s http://localhost:8000/api/health > /dev/null; then
    echo "❌ Backend failed to start. Check the logs above."
    exit 1
fi

echo "✅ Backend is running!"

# Start React Frontend
echo "⚛️ Starting React Frontend..."
cd ..

# Install frontend dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

# Start frontend server
echo "🚀 Starting frontend server on http://localhost:3000"
npm run dev &
FRONTEND_PID=$!

# Wait a moment for frontend to start
sleep 5

echo ""
echo "🎉 SafeRide is now running!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for user to stop
wait 