#!/bin/bash
# Local Build and Launch Script for 5D Interpolator
# This script sets up a complete Python virtual environment and launches both backend and frontend

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"
VENV_DIR="$BACKEND_DIR/venv"

cd "$PROJECT_DIR"

# Banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║        5D Interpolator - Local Build & Launch            ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if port is in use
port_in_use() {
    lsof -i :"$1" >/dev/null 2>&1
}

# Function to kill process on port
kill_port() {
    local port=$1
    echo "Killing process on port $port..."
    lsof -i :"$port" | grep LISTEN | awk '{print $2}' | xargs kill -9 2>/dev/null || true
    sleep 1
}

# Step 1: Prerequisites Check
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 1/6: Checking Prerequisites${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check Python
if ! command_exists python3; then
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python $PYTHON_VERSION${NC}"

# Check pip
if ! command_exists pip3; then
    echo -e "${RED}✗ pip3 is not installed${NC}"
    echo "Please install pip3 and try again"
    exit 1
fi

PIP_VERSION=$(pip3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ pip $PIP_VERSION${NC}"

# Check Node.js
if ! command_exists node; then
    echo -e "${RED}✗ Node.js is not installed${NC}"
    echo "Please install Node.js 18+ and try again"
    exit 1
fi

NODE_VERSION=$(node --version)
echo -e "${GREEN}✓ Node.js $NODE_VERSION${NC}"

# Check npm
if ! command_exists npm; then
    echo -e "${RED}✗ npm is not installed${NC}"
    echo "Please install npm and try again"
    exit 1
fi

NPM_VERSION=$(npm --version)
echo -e "${GREEN}✓ npm $NPM_VERSION${NC}"

echo ""

# Step 2: Port Configuration
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 2/6: Configuring Ports${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

BACKEND_PORT=8000
FRONTEND_PORT=3000

echo -e "${CYAN}  Backend Port:  $BACKEND_PORT${NC}"
echo -e "${CYAN}  Frontend Port: $FRONTEND_PORT${NC}"

# Check and clear ports if necessary
if port_in_use $BACKEND_PORT; then
    echo -e "${YELLOW}⚠ Port $BACKEND_PORT is in use${NC}"
    kill_port $BACKEND_PORT
    echo -e "${GREEN}✓ Port $BACKEND_PORT cleared${NC}"
else
    echo -e "${GREEN}✓ Port $BACKEND_PORT is available${NC}"
fi

if port_in_use $FRONTEND_PORT; then
    echo -e "${YELLOW}⚠ Port $FRONTEND_PORT is in use${NC}"
    kill_port $FRONTEND_PORT
    echo -e "${GREEN}✓ Port $FRONTEND_PORT cleared${NC}"
else
    echo -e "${GREEN}✓ Port $FRONTEND_PORT is available${NC}"
fi

echo ""

# Step 3: Backend Setup with Virtual Environment
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 3/6: Setting Up Backend (Virtual Environment)${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

cd "$BACKEND_DIR"

# Check if venv exists and if we should recreate it
if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Virtual environment already exists${NC}"
    # Check if NumPy is broken by trying a quick import test
    if ! "$VENV_DIR/bin/python" -c "import numpy" 2>/dev/null; then
        echo -e "${YELLOW}Detected broken dependencies, recreating virtual environment...${NC}"
        rm -rf "$VENV_DIR"
        python3 -m venv venv
        echo -e "${GREEN}✓ Virtual environment recreated${NC}"
    else
        echo -e "${GREEN}✓ Virtual environment is healthy${NC}"
    fi
else
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip in virtual environment
echo "Upgrading pip in virtual environment..."
pip install --quiet --upgrade pip

# Install backend dependencies
echo "Installing backend dependencies..."
pip install --quiet -r requirements.txt

# Fix NumPy binary issues by reinstalling from scratch
echo "Ensuring NumPy is properly installed..."
pip uninstall -y numpy 2>/dev/null || true
pip install --no-cache-dir numpy>=1.24.0

# Install fivedreg package in editable mode
echo "Installing fivedreg package..."
pip install --quiet -e .

echo -e "${GREEN}✓ Backend setup complete${NC}"

# Create necessary directories
mkdir -p uploaded_datasets
echo -e "${GREEN}✓ Backend directories created${NC}"

echo ""

# Step 4: Frontend Setup
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 4/6: Setting Up Frontend${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

cd "$FRONTEND_DIR"

# Download and install nvm:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

# in lieu of restarting the shell
\. "$HOME/.nvm/nvm.sh"
# Download and install Node.js:
nvm install 24

npm install

npm run build 
# Install or update frontend dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies (this may take a few minutes)..."
    npm install 
    echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Frontend dependencies already installed${NC}"
    echo "  (run 'cd frontend && npm install' to update)"
fi



echo ""

# Step 5: Start Services
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 5/6: Starting Services${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Create log directory
mkdir -p "$PROJECT_DIR/logs"

# Start backend in virtual environment
echo "Starting backend server..."
cd "$BACKEND_DIR"
# Use explicit path to venv's uvicorn to avoid conflicts with Anaconda
# Exclude venv and build artifacts from file watching to prevent unnecessary reloads
nohup "$VENV_DIR/bin/python" -m uvicorn main:app --reload --reload-exclude "venv/*" --reload-exclude "*.egg-info/*" --reload-exclude "__pycache__/*" --host 0.0.0.0 --port $BACKEND_PORT > "$PROJECT_DIR/logs/backend.log" 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > "$PROJECT_DIR/logs/backend.pid"
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"

# Wait for backend to start
sleep 3

# Start frontend
echo "Starting frontend server..."
cd "$FRONTEND_DIR"
nohup npm run dev > "$PROJECT_DIR/logs/frontend.log" 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > "$PROJECT_DIR/logs/frontend.pid"
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"

echo ""

# Step 6: Verification
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 6/6: Verifying Services${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo "Waiting for services to be ready..."
sleep 5

# Verify backend
echo "Verifying backend..."
if curl -s http://localhost:$BACKEND_PORT/health > /dev/null; then
    echo -e "${GREEN}✓ Backend is responding${NC}"
else
    echo -e "${YELLOW}⚠ Backend may still be starting...${NC}"
    echo "Check logs at: $PROJECT_DIR/logs/backend.log"
fi

# Verify frontend
echo "Verifying frontend..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:$FRONTEND_PORT | grep -q "200\|304"; then
    echo -e "${GREEN}✓ Frontend is responding${NC}"
else
    echo -e "${YELLOW}⚠ Frontend may still be starting...${NC}"
    echo "Check logs at: $PROJECT_DIR/logs/frontend.log"
fi

echo ""

# Display results
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ Build & Launch Complete! Services are running.${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}Access your application at:${NC}"
echo ""
echo -e "  ${GREEN}Frontend:${NC}          http://localhost:$FRONTEND_PORT"
echo -e "  ${GREEN}Backend API:${NC}       http://localhost:$BACKEND_PORT"
echo -e "  ${GREEN}API Documentation:${NC} http://localhost:$BACKEND_PORT/docs"
echo ""
echo -e "${BLUE}Process Information:${NC}"
echo ""
echo -e "  Backend PID:  $BACKEND_PID"
echo -e "  Frontend PID: $FRONTEND_PID"
echo ""
echo -e "${BLUE}Log Files:${NC}"
echo ""
echo -e "  Backend:  $PROJECT_DIR/logs/backend.log"
echo -e "  Frontend: $PROJECT_DIR/logs/frontend.log"
echo ""
echo -e "${BLUE}Useful Commands:${NC}"
echo ""
echo -e "  View backend logs:   ${YELLOW}tail -f logs/backend.log${NC}"
echo -e "  View frontend logs:  ${YELLOW}tail -f logs/frontend.log${NC}"
echo -e "  Stop all services:   ${YELLOW}./scripts/local-stop.sh${NC}"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${CYAN}Virtual Environment Info:${NC}"
echo -e "  Location: $VENV_DIR"
echo -e "  Python:   $(source $VENV_DIR/bin/activate && python --version)"
echo -e "  Pip:      $(source $VENV_DIR/bin/activate && pip --version | cut -d' ' -f1-2)"
echo ""
echo -e "${GREEN}Great Coursework! 🚀${NC}"
echo ""
