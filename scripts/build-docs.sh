#!/bin/bash
# Documentation Build Script for 5D Interpolator
# Builds Sphinx documentation and opens in browser

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
DOCS_DIR="$PROJECT_DIR/docs"
BUILD_DIR="$DOCS_DIR/build"
SOURCE_DIR="$DOCS_DIR/source"

cd "$PROJECT_DIR"

# Banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║        5D Interpolator - Documentation Builder           ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Check if docs directory exists
if [ ! -d "$DOCS_DIR" ]; then
    echo -e "${RED}Error: Documentation directory not found at $DOCS_DIR${NC}"
    exit 1
fi

# Step 1: Check Python
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 1/4: Checking Python installation${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.12+ and try again"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
echo ""

# Step 2: Install Sphinx and dependencies
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 2/5: Installing Sphinx and dependencies${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Create virtual environment for docs if it doesn't exist
if [ ! -d "$DOCS_DIR/venv" ]; then
    echo "Creating virtual environment for documentation..."
    python3 -m venv "$DOCS_DIR/venv"
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
source "$DOCS_DIR/venv/bin/activate"

# Install/upgrade documentation requirements
echo "Installing Sphinx and extensions..."
pip install --quiet --upgrade pip
pip install --quiet -r "$DOCS_DIR/requirements.txt"
echo -e "${GREEN}✓ Sphinx dependencies installed${NC}"
echo ""

# Step 2.5: Install fivedreg package for autodoc
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 2.5/5: Installing fivedreg package${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

BACKEND_DIR="$PROJECT_DIR/backend"
if [ -d "$BACKEND_DIR" ] && [ -f "$BACKEND_DIR/pyproject.toml" ]; then
    echo "Installing fivedreg package in editable mode..."
    pip install --quiet -e "$BACKEND_DIR"
    echo -e "${GREEN}✓ fivedreg package installed${NC}"
else
    echo -e "${YELLOW}⚠ Backend directory not found, skipping package installation${NC}"
fi
echo ""

# Step 3: Build fivedreg package documentation
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 3/5: Building fivedreg package documentation${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

BACKEND_DOCS_DIR="$BACKEND_DIR/docs"
if [ -d "$BACKEND_DOCS_DIR" ]; then
    echo "Building fivedreg package documentation..."
    cd "$BACKEND_DOCS_DIR"

    # Clean backend docs build
    if [ -d "_build" ]; then
        rm -rf "_build"
    fi

    # Build backend documentation
    if sphinx-build -b html . _build/html -q 2>/dev/null; then
        echo -e "${GREEN}✓ fivedreg package documentation built${NC}"
    else
        echo -e "${YELLOW}⚠ fivedreg package documentation build had warnings (continuing)${NC}"
    fi

    cd "$PROJECT_DIR"
else
    echo -e "${YELLOW}⚠ Backend docs directory not found, skipping${NC}"
fi
echo ""

# Step 4: Clean and build main documentation
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 4/5: Building main HTML documentation${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Clean previous build
if [ -d "$BUILD_DIR" ]; then
    echo "Cleaning previous build..."
    rm -rf "$BUILD_DIR"
    echo -e "${GREEN}✓ Previous build cleaned${NC}"
fi

# Build documentation
echo "Building main documentation..."
cd "$DOCS_DIR"

# Run Sphinx build for HTML
if sphinx-build -b html "$SOURCE_DIR" "$BUILD_DIR/html" --keep-going; then
    echo -e "${GREEN}✓ HTML documentation built successfully${NC}"
else
    echo -e "${RED}✗ HTML documentation build failed${NC}"
    echo "Check the error messages above for details"
    deactivate
    exit 1
fi

# Copy backend documentation into main documentation
if [ -d "$BACKEND_DOCS_DIR/_build/html" ]; then
    echo "Integrating fivedreg package documentation..."
    mkdir -p "$BUILD_DIR/html/fivedreg-package"
    cp -r "$BACKEND_DOCS_DIR/_build/html/"* "$BUILD_DIR/html/fivedreg-package/"
    echo -e "${GREEN}✓ Package documentation integrated at /fivedreg-package/${NC}"
fi

# Build PDF automatically
echo ""
echo "Building PDF..."
mkdir -p "$BUILD_DIR/downloads"

if command -v pdflatex &> /dev/null; then
    sphinx-build -b latex "$SOURCE_DIR" "$BUILD_DIR/latex" -q
    cd "$BUILD_DIR/latex"
    for i in 1 2 3; do
        pdflatex -interaction=nonstopmode 5D-Interpolator-Documentation.tex > /dev/null 2>&1 || true
    done
    if [ -f "5D-Interpolator-Documentation.pdf" ]; then
        cp "5D-Interpolator-Documentation.pdf" "../downloads/"
        echo -e "${GREEN}✓ PDF generated${NC}"
    fi
    cd "$DOCS_DIR"
fi

# Build EPUB
echo "Building EPUB..."
sphinx-build -b epub "$SOURCE_DIR" "$BUILD_DIR/epub" -q
# Find the EPUB file (name varies)
EPUB_FILE=$(find "$BUILD_DIR/epub" -name "*.epub" -type f | head -1)
if [ -n "$EPUB_FILE" ]; then
    cp "$EPUB_FILE" "$BUILD_DIR/downloads/5D-Interpolator-Documentation.epub"
    echo -e "${GREEN}✓ EPUB generated${NC}"
fi

# Create HTML archive
echo "Creating HTML archive..."
cd "$BUILD_DIR"
zip -r -q "downloads/5D-Interpolator-Documentation-HTML.zip" html/
echo -e "${GREEN}✓ HTML archive created${NC}"

# Copy download files into HTML directory for easy access
echo "Copying downloads to HTML directory..."
mkdir -p html/downloads
cp downloads/*.pdf html/downloads/ 2>/dev/null || true
cp downloads/*.epub html/downloads/ 2>/dev/null || true
cp downloads/*.zip html/downloads/ 2>/dev/null || true
echo -e "${GREEN}✓ Downloads accessible from HTML${NC}"

cd "$DOCS_DIR"

echo ""

# Step 5: Display results and open browser
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 5/5: Documentation ready${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Get file path for opening
INDEX_FILE="$BUILD_DIR/html/index.html"
FILE_URL="file://$INDEX_FILE"

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ Documentation Build Complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}Documentation is available at:${NC}"
echo ""
echo -e "  ${GREEN}File URL:${NC}     $FILE_URL"
echo -e "  ${GREEN}Local Path:${NC}   $INDEX_FILE"
echo ""
echo -e "${BLUE}Build Information:${NC}"
echo ""
echo -e "  Source:  $SOURCE_DIR"
echo -e "  Output:  $BUILD_DIR/html"
echo ""
echo -e "${BLUE}Documentation Sections:${NC}"
echo ""
echo -e "  Main Documentation:     $BUILD_DIR/html/index.html"
if [ -d "$BUILD_DIR/html/fivedreg-package" ]; then
    echo -e "  Package Documentation:  $BUILD_DIR/html/fivedreg-package/index.html"
fi
echo ""
echo -e "${BLUE}Downloads Available:${NC}"
echo ""
if [ -d "$BUILD_DIR/downloads" ]; then
    ls -lh "$BUILD_DIR/downloads/" 2>/dev/null | grep -v total | awk '{print "  📦 " $9 " (" $5 ")"}'
fi
echo ""

# Deactivate virtual environment
deactivate

# Ask to open in browser
read -p "$(echo -e ${BLUE}Do you want to open the documentation in your browser? [Y/n]:${NC} )" -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo "Opening documentation in browser..."

    # Try to open browser (works on macOS, Linux with xdg-open, and WSL with wslview)
    if command -v open > /dev/null; then
        open "$INDEX_FILE"
    elif command -v xdg-open > /dev/null; then
        xdg-open "$INDEX_FILE"
    elif command -v wslview > /dev/null; then
        wslview "$INDEX_FILE"
    else
        echo -e "${YELLOW}Could not detect browser command. Please open manually:${NC}"
        echo "$FILE_URL"
    fi
fi

echo ""
echo -e "${BLUE}Useful commands:${NC}"
echo ""
echo -e "  View in browser:     ${YELLOW}open $INDEX_FILE${NC}"
echo -e "  Rebuild docs:        ${YELLOW}./scripts/build-docs.sh${NC}"
echo -e "  Clean build:         ${YELLOW}rm -rf docs/build${NC}"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}Documentation build completed successfully! 📚${NC}"
echo ""
