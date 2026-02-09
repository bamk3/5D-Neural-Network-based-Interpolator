# Deployment Guide

## Quick Start

This project includes automated scripts for local deployment and documentation building.

### Prerequisites

- Python 3.12+
- Node.js 20+
- npm

### Local Deployment

Deploy the entire application stack locally:

```bash
./scripts/deploy-local.sh
```

This script will:
1. Check prerequisites (Python, Node.js, npm)
2. Set up environment configuration
3. Check and clear ports (8000, 3000) if needed
4. Set up backend (virtual environment, dependencies)
5. Set up frontend (npm install)
6. Start both services as background processes
7. Create sample datasets automatically
8. Verify services are healthy
9. Open application in your browser

**Sample Datasets Created:**
- `data/sample_training.pkl` - 1000 samples for training
- `data/sample_prediction.pkl` - 100 samples for prediction

### Access the Application

Once deployed, access the application at:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Quick Workflow

1. Open http://localhost:3000/upload
2. Upload `data/sample_training.pkl` as Training dataset
3. Go to Train page and click 'Start Training'
4. Upload `data/sample_prediction.pkl` as Prediction dataset
5. Go to Predict page and generate predictions

### Managing Services


**Stop All Services:**
```bash
./scripts/local-stop.sh
```

**View Logs:**
```bash
# Backend logs
tail -f logs/backend.log

# Frontend logs
tail -f logs/frontend.log
```

## Documentation

Build and view the comprehensive documentation:

```bash
./scripts/build-docs.sh
```

This script will:
1. Create a Python virtual environment for Sphinx
2. Install Sphinx and required extensions
3. Build HTML documentation
4. Open documentation in your browser

The documentation is accessible at:
- **File URL**: file://.../docs/build/html/index.html
- **Local Path**: docs/build/html/index.html

### Documentation Contents

- **Installation Guide** - Setup instructions
- **Quick Start** - Getting started tutorial
- **Usage Guide** - Detailed usage with hyperparameters
- **Dataset Specifications** - Data format requirements
- **API Reference** - Complete REST API documentation
  - Backend endpoints
  - Frontend components
  - Neural network module
- **Testing Guide** - Test suite documentation (52 tests, 74.54% coverage)
- **Deployment Guide** - Local and Docker deployment
- **Architecture** - System design and data flow

## Docker Deployment

### Using Docker Compose

Start the application:
```bash
docker compose up
```

Start in detached mode:
```bash
docker compose up -d
```

Stop the application:
```bash
docker compose down
```

Rebuild containers:
```bash
docker compose build --no-cache
docker compose up
```

### Access Services

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Testing

### Run Backend Tests

```bash
cd backend
source venv/bin/activate
pytest -v
```

### View Test Coverage

```bash
cd backend
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

### Test Results

- **Total Tests**: 52
- **Coverage**: 74.54%
- **Test Categories**:
  - API endpoints (upload, train, predict)
  - Neural network module
  - Data handling
  - Validation logic

## Environment Configuration

The application uses `.env` files for configuration:

```env
# Development Environment
BUILD_TARGET=development
APP_ENV=development
BACKEND_PORT=8000
FRONTEND_PORT=3000
```

## Troubleshooting

### Ports Already in Use

If ports 8000 or 3000 are already in use:

```bash
# Kill processes on these ports
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

Or use the stop script:
```bash
./scripts/stop-local.sh
```

### Backend Not Starting

Check the backend log:
```bash
cat logs/backend.log
```

Common issues:
- Virtual environment not created
- Dependencies not installed
- Port already in use

Solution:
```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Not Starting

Check the frontend log:
```bash
cat logs/frontend.log
```

Common issues:
- node_modules not installed
- Port already in use
- Node version incompatible

Solution:
```bash
cd frontend
rm -rf node_modules
npm install
```

### Documentation Build Fails

Ensure Python 3 is installed:
```bash
python3 --version
```

Rebuild documentation:
```bash
cd docs
rm -rf build venv
./build-docs.sh
```

## Directory Structure

```
interpolator/
├── backend/              # FastAPI backend
│   ├── main.py          # API server
│   ├── fivedreg/        # Neural network package
│   ├── tests/           # Test suite
│   └── venv/            # Python virtual environment
├── frontend/            # Next.js frontend
│   ├── src/app/         # React pages
│   └── node_modules/    # npm dependencies
├── docs/                # Sphinx documentation
│   ├── source/          # Documentation source
│   ├── build/           # Generated HTML
│   └── venv/            # Sphinx virtual environment
├── scripts/             # Deployment scripts
│   ├── deploy-local.sh  # Local deployment
│   ├── stop-local.sh    # Stop services
│   ├── status-local.sh  # Check status
│   └── build-docs.sh    # Build documentation
├── data/                # Sample datasets
│   ├── sample_training.pkl
│   └── sample_prediction.pkl
├── logs/                # Service logs
│   ├── backend.log
│   └── frontend.log
├── .env                 # Environment configuration
└── docker-compose.yml   # Docker orchestration
```

## Performance

### Training Speed

- 100 samples: ~5 seconds
- 1,000 samples: ~15 seconds
- 10,000 samples: ~45 seconds
- 100,000 samples: ~5 minutes

### Recommended Dataset Sizes

- Minimum: 100 samples
- Optimal: 1,000-10,000 samples
- Maximum: No hard limit (training time increases)

## Support

For issues or questions:
1. Check the documentation: `./scripts/build-docs.sh`
2. Review logs in `logs/` directory
3. Check test results: `cd backend && pytest -v`

## License

This is a coursework project for the DIS course at the University of Cambridge.

Author: Makimona Kiakisolako (bamk3)
