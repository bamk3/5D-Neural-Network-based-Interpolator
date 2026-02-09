#!/bin/bash
# Build PDF Documentation Script
# Generates PDF documentation using Sphinx and LaTeX

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DOCS_DIR="$PROJECT_DIR/docs"
BUILD_DIR="$DOCS_DIR/build"
SOURCE_DIR="$DOCS_DIR/source"

cd "$PROJECT_DIR"

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║        5D Interpolator - PDF Documentation Builder       ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Check prerequisites
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 1/5: Checking Prerequisites${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python $(python3 --version | cut -d' ' -f2)${NC}"

# Check for LaTeX installation
if command -v pdflatex &> /dev/null; then
    echo -e "${GREEN}✓ pdflatex found${NC}"
    LATEX_AVAILABLE=true
else
    echo -e "${YELLOW}⚠ pdflatex not found - PDF generation will use rst2pdf fallback${NC}"
    LATEX_AVAILABLE=false
fi

echo ""

# Setup virtual environment
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 2/5: Setting Up Environment${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

if [ ! -d "$DOCS_DIR/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$DOCS_DIR/venv"
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

source "$DOCS_DIR/venv/bin/activate"

# Install dependencies
echo "Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r "$DOCS_DIR/requirements.txt"

# Install rst2pdf for fallback PDF generation
if [ "$LATEX_AVAILABLE" = false ]; then
    echo "Installing rst2pdf for PDF generation..."
    pip install --quiet rst2pdf
fi

echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Build LaTeX/PDF
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 3/5: Building PDF Documentation${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

cd "$DOCS_DIR"

if [ "$LATEX_AVAILABLE" = true ]; then
    echo "Building with LaTeX (pdflatex)..."

    # Clean previous build
    rm -rf "$BUILD_DIR/latex"

    # Build LaTeX
    if sphinx-build -b latex "$SOURCE_DIR" "$BUILD_DIR/latex" -q; then
        echo -e "${GREEN}✓ LaTeX files generated${NC}"

        # Compile PDF
        echo "Compiling PDF..."
        cd "$BUILD_DIR/latex"

        # Run pdflatex multiple times for proper references
        for i in 1 2 3; do
            pdflatex -interaction=nonstopmode 5D-Interpolator-Documentation.tex > /dev/null 2>&1 || true
        done

        if [ -f "5D-Interpolator-Documentation.pdf" ]; then
            PDF_SIZE=$(du -h "5D-Interpolator-Documentation.pdf" | cut -f1)
            echo -e "${GREEN}✓ PDF compiled successfully (${PDF_SIZE})${NC}"
            PDF_PATH="$BUILD_DIR/latex/5D-Interpolator-Documentation.pdf"
        else
            echo -e "${RED}✗ PDF compilation failed${NC}"
            exit 1
        fi
    else
        echo -e "${RED}✗ LaTeX build failed${NC}"
        exit 1
    fi
else
    echo "Building with rst2pdf (fallback)..."

    # Add rst2pdf to conf.py extensions temporarily
    cd "$DOCS_DIR"

    # Build with rst2pdf
    if sphinx-build -b pdf "$SOURCE_DIR" "$BUILD_DIR/pdf" -q 2>/dev/null; then
        echo -e "${GREEN}✓ PDF generated with rst2pdf${NC}"
        PDF_PATH="$BUILD_DIR/pdf/5D-Interpolator-Documentation.pdf"
    else
        echo -e "${YELLOW}⚠ rst2pdf build had warnings, but PDF may be generated${NC}"
        PDF_PATH="$BUILD_DIR/pdf/5D-Interpolator-Documentation.pdf"
    fi
fi

echo ""

# Build HTML archive
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 4/5: Creating HTML Archive${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

cd "$PROJECT_DIR"

# Build HTML if not already built
if [ ! -d "$BUILD_DIR/html" ]; then
    echo "Building HTML documentation..."
    sphinx-build -b html "$SOURCE_DIR" "$BUILD_DIR/html" -q
fi

# Create downloads directory
mkdir -p "$BUILD_DIR/downloads"

# Create HTML archive
echo "Creating HTML archive..."
cd "$BUILD_DIR"
tar -czf "downloads/5D-Interpolator-Documentation-HTML.tar.gz" html/
ZIP_SIZE=$(du -h "downloads/5D-Interpolator-Documentation-HTML.tar.gz" | cut -f1)
echo -e "${GREEN}✓ HTML archive created (${ZIP_SIZE})${NC}"

# Also create a zip file
if command -v zip &> /dev/null; then
    cd html
    zip -r -q "../downloads/5D-Interpolator-Documentation-HTML.zip" .
    ZIP_SIZE=$(du -h "../downloads/5D-Interpolator-Documentation-HTML.zip" | cut -f1)
    echo -e "${GREEN}✓ HTML zip archive created (${ZIP_SIZE})${NC}"
fi

echo ""

# Copy PDF to downloads
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Step 5/5: Organizing Downloads${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

if [ -f "$PDF_PATH" ]; then
    cp "$PDF_PATH" "$BUILD_DIR/downloads/"
    echo -e "${GREEN}✓ PDF copied to downloads directory${NC}"
fi

# Create README for downloads
cat > "$BUILD_DIR/downloads/README.txt" << 'EOF'
5D Neural Network Interpolator - Documentation Downloads
========================================================

This directory contains downloadable documentation in multiple formats:

PDF Documentation:
  - 5D-Interpolator-Documentation.pdf
    Complete documentation in PDF format
    Suitable for printing and offline reading

HTML Documentation Archives:
  - 5D-Interpolator-Documentation-HTML.tar.gz
    Compressed archive (tar.gz) of HTML documentation
    Extract and open index.html in a web browser

  - 5D-Interpolator-Documentation-HTML.zip
    Compressed archive (zip) of HTML documentation
    Extract and open index.html in a web browser

Usage:
  PDF: Open directly in any PDF reader
  HTML: Extract archive, then open index.html in a browser

Generated: $(date)
Version: 0.1.0
Author: Makimona Kiakisolako (bamk3)
EOF

echo -e "${GREEN}✓ README created${NC}"

echo ""

# Summary
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ Documentation Build Complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}Downloads available at:${NC}"
echo ""
echo -e "  ${GREEN}Directory:${NC} $BUILD_DIR/downloads/"
echo ""
echo -e "${BLUE}Available files:${NC}"
ls -lh "$BUILD_DIR/downloads/" | grep -v total | awk '{print "  - " $9 " (" $5 ")"}'
echo ""
echo -e "${BLUE}Quick access:${NC}"
echo -e "  PDF:  ${YELLOW}open $BUILD_DIR/downloads/5D-Interpolator-Documentation.pdf${NC}"
echo -e "  HTML: ${YELLOW}open $BUILD_DIR/html/index.html${NC}"
echo ""

# Open PDF if requested
read -p "$(echo -e ${BLUE}Do you want to open the PDF now? [Y/n]:${NC} )" -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    if [ -f "$BUILD_DIR/downloads/5D-Interpolator-Documentation.pdf" ]; then
        open "$BUILD_DIR/downloads/5D-Interpolator-Documentation.pdf" 2>/dev/null || \
        xdg-open "$BUILD_DIR/downloads/5D-Interpolator-Documentation.pdf" 2>/dev/null || \
        echo "Please open: $BUILD_DIR/downloads/5D-Interpolator-Documentation.pdf"
    fi
fi

echo ""
echo -e "${GREEN}Build complete! 📚${NC}"
echo ""
