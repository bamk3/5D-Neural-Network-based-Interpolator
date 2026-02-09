#!/bin/bash
# Stop script for 5D Interpolator
# Gracefully stops all Docker services

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
echo "║         5D Interpolator - Stop Services Script            ║"
echo "║                       by bamk3                            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Check if services are running
if ! docker compose ps | grep -q "Up"; then
    echo -e "${YELLOW}No running interpolator services found.${NC}"
    echo ""
    exit 0
fi

# Show current status
echo -e "${BLUE}Current interpolator service status:${NC}"
docker compose ps
echo ""

# Ask for confirmation
echo -e "${YELLOW}This will stop the interpolator services (backend & frontend).${NC}"
echo -e "${GREEN}Note: Other Docker containers on your system will NOT be affected.${NC}"
#read -p "$(echo -e ${BLUE}Continue? [Y/n]:${NC} )" -n 1 -r


# Stop services
echo ""
echo -e "${YELLOW}Stopping services...${NC}"
docker compose down

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ Interpolator services stopped successfully${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}To start services again, run:${NC}"
echo -e "  ${YELLOW}./scripts/docker-start.sh${NC}"
echo ""

