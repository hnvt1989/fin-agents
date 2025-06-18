#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting Financial Planner Application...${NC}\n"

# Function to kill processes on exit
cleanup() {
    echo -e "\n${RED}Stopping all servers...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

# Set up trap to call cleanup on script exit
trap cleanup EXIT INT TERM

# Start backend server
echo -e "${GREEN}Starting Python backend server...${NC}"
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies if requirements.txt exists and pip list is empty
if [ -f "requirements.txt" ]; then
    if ! pip freeze | grep -q fastapi; then
        echo -e "${BLUE}Installing Python dependencies...${NC}"
        pip install -r requirements.txt
    fi
fi

# Start the backend
python main.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 5

# Start frontend server
echo -e "${GREEN}Starting React frontend server...${NC}"
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo -e "\n${BLUE}Both servers are running!${NC}"
echo -e "${GREEN}Backend:${NC} http://localhost:8000"
echo -e "${GREEN}Frontend:${NC} http://localhost:3000"
echo -e "\n${BLUE}Press Ctrl+C to stop all servers${NC}\n"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID