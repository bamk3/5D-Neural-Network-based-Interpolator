#!/bin/bash
# Stop Local Services Script for 5D Interpolator

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")\" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo -e "${BLUE}Stopping 5D Interpolator services...${NC}"
echo ""

# Stop backend
if [ -f "logs/backend.pid" ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if ps -p $BACKEND_PID > /dev/null; then
        echo "Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
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
    if ps -p $FRONTEND_PID > /dev/null; then
        echo "Stopping frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        rm logs/frontend.pid
        echo -e "${GREEN}✓ Frontend stopped${NC}"
    else
        echo -e "${YELLOW}Frontend process not running${NC}"
        rm logs/frontend.pid
    fi
else
    echo -e "${YELLOW}No frontend PID file found${NC}"
fi

# Kill any remaining processes on default ports
echo ""
echo "Cleaning up ports..."
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9 2>/dev/null || true
lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9 2>/dev/null || true

echo ""
echo -e "${GREEN}✓ All services stopped${NC}"
echo ""
