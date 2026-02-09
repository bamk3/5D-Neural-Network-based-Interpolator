#!/bin/bash
# Convenience script for running tests

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$PROJECT_DIR/backend"

set -e  # Exit on error

echo "================================"
echo "5D Interpolator - Test Runner"
echo "================================"
echo ""
cd "$BACKEND_DIR"
# Check if we're in the backend directory
if [ ! -f "main.py" ]; then
    echo "Error: Please run this script from the backend directory"
    exit 1
fi

pip install -r requirements-dev.txt
# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "pytest not found. Installing test dependencies..."
    pip install -r requirements-dev.txt
fi

# Parse command line arguments
case "$1" in
    "fast")
        echo "Running fast tests only..."
        pytest -m "not slow" -v
        ;;
    "unit")
        echo "Running unit tests..."
        pytest -m unit -v
        ;;
    "integration")
        echo "Running integration tests..."
        pytest -m integration -v
        ;;
    "coverage")
        echo "Running tests with coverage report..."
        pytest --cov=. --cov-report=html --cov-report=term-missing -v
        echo ""
        echo "Coverage report generated in coverage_html/index.html"
        ;;
    "parallel")
        echo "Running tests in parallel..."
        pytest -n auto -v
        ;;
    "verbose")
        echo "Running all tests with verbose output..."
        pytest -vv
        ;;
    "quiet")
        echo "Running tests in quiet mode..."
        pytest -q
        ;;
    "failed")
        echo "Re-running last failed tests..."
        pytest --lf -v
        ;;
    "help"|"-h"|"--help")
        echo "Usage: ./run_tests.sh [option]"
        echo ""
        echo "Options:"
        echo "  (no args)     Run all tests"
        echo "  fast          Run only fast tests (skip slow tests)"
        echo "  unit          Run only unit tests"
        echo "  integration   Run only integration tests"
        echo "  coverage      Run tests with coverage report"
        echo "  parallel      Run tests in parallel (faster)"
        echo "  verbose       Run with extra verbose output"
        echo "  quiet         Run in quiet mode"
        echo "  failed        Re-run only failed tests from last run"
        echo "  help          Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./run_tests.sh              # Run all tests"
        echo "  ./run_tests.sh fast         # Run fast tests only"
        echo "  ./run_tests.sh coverage     # Generate coverage report"
        ;;
    "")
        echo "Running all tests..."
        pytest -v
        ;;
    *)
        echo "Unknown option: $1"
        echo "Run './run_tests.sh help' for usage information"
        exit 1
        ;;
esac

echo ""
echo "================================"
echo "Tests completed!"
echo "================================"
