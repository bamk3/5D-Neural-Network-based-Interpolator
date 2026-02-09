#!/bin/bash
# Stop Local Services Script for 5D Interpolator
# This script cleanly stops all running backend and frontend services

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo -e "${BLUE}Stopping 5D Interpolator services...${NC}"
echo ""

# Stop backend
if [ -f "logs/backend.pid" ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null || true
        # Wait for process to terminate gracefully
        sleep 2
        # Force kill if still running
        if ps -p $BACKEND_PID > /dev/null 2>&1; then
            kill -9 $BACKEND_PID 2>/dev/null || true
        fi
        rm logs/backend.pid
        echo -e "${GREEN}✓ Backend stopped${NC}"
    else
        echo -e "${YELLOW}Backend process not running${NC}"
        rm logs/backend.pid
    fi
else
    echo -e "${YELLOW}No backend PID file found${NC}"
fi

# Stop frontend
if [ -f "logs/frontend.pid" ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "Stopping frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID 2>/dev/null || true
        # Wait for process to terminate gracefully
        sleep 2
        # Force kill if still running
        if ps -p $FRONTEND_PID > /dev/null 2>&1; then
            kill -9 $FRONTEND_PID 2>/dev/null || true
        fi
        rm logs/frontend.pid
        echo -e "${GREEN}✓ Frontend stopped${NC}"
    else
        echo -e "${YELLOW}Frontend process not running${NC}"
        rm logs/frontend.pid
    fi
else
    echo -e "${YELLOW}No frontend PID file found${NC}"
fi

# Kill any remaining processes on default ports (cleanup)
echo ""
echo "Cleaning up ports..."

# Check and kill port 8000 (backend)
if lsof -i :8000 >/dev/null 2>&1; then
    lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9 2>/dev/null || true
    echo -e "${GREEN}✓ Port 8000 cleaned${NC}"
fi

# Check and kill port 3000 (frontend)
if lsof -i :3000 >/dev/null 2>&1; then
    lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9 2>/dev/null || true
    echo -e "${GREEN}✓ Port 3000 cleaned${NC}"
fi

echo ""
echo -e "${GREEN}✓ All services stopped${NC}"
echo ""
