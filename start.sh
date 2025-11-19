#!/bin/bash

# Start script for Todoer application
# This script starts both the backend and frontend services

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Todoer Application...${NC}\n"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  Warning: .env file not found${NC}"
    echo "Creating .env file with default values..."
    cat > .env << EOF
SECRET_KEY=your-secret-key-change-in-production-$(openssl rand -hex 16)
OPENAI_API_KEY=your-openai-api-key
API_BASE_URL=http://localhost:8000
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
EOF
    echo -e "${YELLOW}Please update .env with your actual values, especially OPENAI_API_KEY${NC}\n"
fi

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}Shutting down services...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit
}

trap cleanup SIGINT SIGTERM

# Check if backend dependencies are installed
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Installing Python dependencies...${NC}"
    uv sync
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}Installing frontend dependencies...${NC}"
    cd frontend
    npm install
    cd ..
fi

# Start backend
echo -e "${GREEN}Starting backend server...${NC}"
uv run python run_backend.py &
BACKEND_PID=$!

# Wait for backend to be ready
echo -e "${BLUE}Waiting for backend to start...${NC}"
sleep 3

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${YELLOW}Backend failed to start. Check logs above.${NC}"
    exit 1
fi

# Start frontend
echo -e "${GREEN}Starting frontend server...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo -e "\n${GREEN}✅ Services started successfully!${NC}\n"
echo -e "${BLUE}Backend API:${NC} http://localhost:8000"
echo -e "${BLUE}API Docs:${NC} http://localhost:8000/docs"
echo -e "${BLUE}Frontend:${NC} http://localhost:3000"
echo -e "\n${YELLOW}Press Ctrl+C to stop all services${NC}\n"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID

