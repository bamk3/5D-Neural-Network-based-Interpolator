#!/bin/bash
# Complete setup script for 5D Interpolator
# This script cleans, rebuilds, and starts all services from scratch

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

# Banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║        5D Interpolator - Complete Setup Script            ║"
echo "║                       by bamk3                            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running!${NC}"
    echo ""

    # Detect platform and provide appropriate instructions
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo -e "${YELLOW}On Linux, start the Docker service:${NC}"
        echo ""
        echo "  sudo systemctl start docker"
        echo "  sudo systemctl enable docker  # Enable on boot"
        echo ""
        echo -e "${BLUE}Or if using Docker Desktop for Linux:${NC}"
        echo "  systemctl --user start docker-desktop"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "${YELLOW}On macOS, start Docker Desktop:${NC}"
        echo "  open -a Docker"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        echo -e "${YELLOW}On Windows, start Docker Desktop from the Start menu${NC}"
    else
        echo -e "${YELLOW}Please start Docker and try again.${NC}"
    fi

    echo ""
    exit 1
fi

# Step 1: Clean
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 1/3: Cleaning up existing containers and volumes${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check if environment file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}No .env file found. Creating from .env.development${NC}"
    cp .env.development .env
    echo -e "${GREEN}✓ Created .env file${NC}"
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

echo "Stopping and removing containers, networks, and volumes..."
docker compose down -v --remove-orphans 2>/dev/null || true
echo -e "${GREEN}✓ Cleanup complete${NC}"
echo ""


# Step 2: Rebuild
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 2/3: Rebuilding Docker images from scratch${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "This may take 3-6 minutes..."
echo ""

docker compose build --no-cache

echo ""
echo -e "${GREEN}✓ Images rebuilt successfully${NC}"
echo ""

# Step 3: Start
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 3/3: Starting services${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

docker compose up -d

echo ""
echo "Waiting for services to be healthy..."
sleep 5

# Check service health
echo ""
echo -e "${BLUE}Checking service status...${NC}"
docker compose ps
echo ""

# Display service URLs
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ Setup Complete! Services are running.${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}Access your application at:${NC}"
echo ""
echo -e "  ${GREEN}Frontend:${NC}     http://localhost:${FRONTEND_PORT:-3000}"
echo -e "  ${GREEN}Backend API:${NC}  http://localhost:${BACKEND_PORT:-8000}"
echo -e "  ${GREEN}API Docs:${NC}     http://localhost:${BACKEND_PORT:-8000}/docs"
echo ""
echo -e "${BLUE}Useful commands:${NC}"
echo ""
#echo -e "  View logs:           ${YELLOW}./scripts/docker-dev.sh logs${NC}"
#echo -e "  Backend logs:        ${YELLOW}./scripts/docker-dev.sh logs-backend${NC}"
#echo -e "  Frontend logs:       ${YELLOW}./scripts/docker-dev.sh logs-frontend${NC}"
echo -e "  Stop services:       ${YELLOW}./scripts/docker-stop.sh${NC}"
#echo -e "  Restart services:    ${YELLOW}./scripts/docker-dev.sh restart${NC}"
#echo -e "  Backend shell:       ${YELLOW}./scripts/docker-dev.sh shell-backend${NC}"
#echo -e "  Run tests:           ${YELLOW}./scripts/docker-dev.sh test-backend${NC}"
echo ""
echo -e "${BLUE}Quick reference:${NC}"
echo -e "  Fresh start:         ${YELLOW}./scripts/docker-start.sh${NC}    (3-6 min, cleans everything)"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Skip opening browser automatically (users can open manually)
echo -e "${BLUE}Open the application in your browser:${NC} http://localhost:${FRONTEND_PORT:-3000}"

echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
echo ""
