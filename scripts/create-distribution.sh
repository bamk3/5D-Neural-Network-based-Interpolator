#!/bin/bash
# Create distribution package for sharing with third parties
# Excludes all generated/build files

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

# Output filename
OUTPUT_FILE="5D-Interpolator-Source.tar.gz"

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                           ║${NC}"
echo -e "${BLUE}║        Creating Distribution Package                     ║${NC}"
echo -e "${BLUE}║                                                           ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if git is available
if command -v git &> /dev/null && [ -d .git ]; then
    echo -e "${YELLOW}Using git archive (recommended)...${NC}"
    git archive --format=tar.gz --output="$OUTPUT_FILE" HEAD
    echo -e "${GREEN}✓ Created: $OUTPUT_FILE${NC}"
else
    echo -e "${YELLOW}Git not available, using tar with exclusions...${NC}"

    tar -czf "$OUTPUT_FILE" \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        --exclude='*.pyo' \
        --exclude='*.pyd' \
        --exclude='node_modules' \
        --exclude='.next' \
        --exclude='out' \
        --exclude='venv' \
        --exclude='env' \
        --exclude='ENV' \
        --exclude='*.egg-info' \
        --exclude='build' \
        --exclude='dist' \
        --exclude='.pytest_cache' \
        --exclude='.coverage' \
        --exclude='coverage_html' \
        --exclude='htmlcov' \
        --exclude='docs/build' \
        --exclude='docs/_build' \
        --exclude='docs/venv' \
        --exclude='uploaded_datasets' \
        --exclude='data' \
        --exclude='benchmark_results' \
        --exclude='.DS_Store' \
        --exclude='Thumbs.db' \
        --exclude='.claude' \
        --exclude='.vscode' \
        --exclude='.idea' \
        --exclude='*.swp' \
        --exclude='*.swo' \
        --exclude='*.log' \
        --exclude='.env' \
        --exclude='backend/.env' \
        --exclude='frontend/.env.local' \
        .

    echo -e "${GREEN}✓ Created: $OUTPUT_FILE${NC}"
fi

# Get file size
FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ Distribution Package Created Successfully${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}Package Details:${NC}"
echo -e "  File:     ${YELLOW}$OUTPUT_FILE${NC}"
echo -e "  Size:     ${YELLOW}$FILE_SIZE${NC}"
echo -e "  Location: ${YELLOW}$PROJECT_DIR/$OUTPUT_FILE${NC}"
echo ""
echo -e "${BLUE}What's Included:${NC}"
echo -e "  ✓ All source code (.py, .tsx, .ts)"
echo -e "  ✓ Configuration files (.toml, .json, .yml)"
echo -e "  ✓ Scripts (.sh)"
echo -e "  ✓ Documentation source (.rst, .md)"
echo -e "  ✓ Dockerfiles and compose files"
echo ""
echo -e "${BLUE}What's Excluded:${NC}"
echo -e "  ✗ node_modules/ (600+ MB)"
echo -e "  ✗ Build artifacts (__pycache__, .next, dist)"
echo -e "  ✗ Virtual environments (venv/)"
echo -e "  ✗ Documentation builds (docs/build/)"
echo -e "  ✗ Test artifacts (.pytest_cache, .coverage)"
echo -e "  ✗ User data (uploaded_datasets/)"
echo ""
echo -e "${YELLOW}Recipients can rebuild everything with:${NC}"
echo -e "  1. Extract: ${BLUE}tar -xzf $OUTPUT_FILE${NC}"
echo -e "  2. Build:   ${BLUE}./scripts/docker-start.sh${NC}"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
