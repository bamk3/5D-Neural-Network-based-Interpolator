# 5D Neural Network Interpolator

This is an application for 5D interpolation using neural networks, developed by Mak Kiakisolako (bamk3) as coursework for the DIS course at the University of Cambridge.

## 🚀 Quick Start


### Option 1: Using Docker (Recommended for Production)

```bash
# Complete setup from scratch
./scripts/docker-start.sh
```

**Prerequisites:**
- Docker Desktop installed and running

**That's it!** Access your application at:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs




### Option 2: Local Development (No Docker Required)

**Recommended for development - fastest startup and easiest debugging:**
```bash
# One command to install dependencies and launch the entire technology stack.
./scripts/local-build.sh
```

**Prerequisites:**
- Python 3.8+ installed
- Node.js 18+ installed
- npm and pip3 available

**Voilà!** The script will:
- Create a Python virtual environment
- Install all Python dependencies
- Install all Node.js dependencies
- Start both backend and frontend servers
- Show real-time logs

Access the application at:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

**To stop:** Press `Ctrl+C` or run `./scripts/local-stop.sh`

### Option 3: Manual Setup

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📖 Documentation

### Testing
- **[backend/tests/README.md](backend/tests/README.md)** - Testing guide
- **[backend/tests/TESTING_SUMMARY.md](backend/tests/TESTING_SUMMARY.md)** - Test results

### Scripts & Development
- **[scripts/README.md](scripts/README.md)** - Available scripts reference
- **[scripts/local-build.sh](scripts/local-build.sh)** - Local development setup script

## 🏗️ Project Structure

```
interpolator/
├── backend/                # FastAPI backend
│   ├── main.py            # API server
│   ├── fivedreg/          # Neural network package
│   ├── tests/             # Test suite (52 tests, 74% coverage)
│   └── Dockerfile         # Backend container
├── frontend/              # Next.js 16 frontend
│   ├── src/               # Source code
│   └── Dockerfile         # Frontend container
├── scripts/               # Helper scripts
│   ├── local-build.sh    # Local setup script (no Docker)
│   ├── docker-start.sh   # Complete Docker setup
│   ├── docker-dstop.sh   # stop the Docker container
│   └── local-stop.sh     # to stop services running locally
|   └── build-docs.sh     # to build the docs locally
|   └── run_tests.sh      # to run the all the tests 
├── docker-compose.yml     # Service orchestration
└── .env.example          # Environment variables template
```

## 🔧 Common Commands

### Local Development (No Docker)

| Task | Command | Speed |
|------|---------|-------|
| **Complete local setup** | `./scripts/local-build.sh` | 2-3 min |
| **Stop all services** | `./scripts/local-stop.sh` or `Ctrl+C` | 1 sec |
| **View backend logs** | `tail -f logs/backend.log` | - |
| **View frontend logs** | `tail -f logs/frontend.log` | - |

### Docker Commands

| Task | Command | Speed |
|------|---------|-------|
| **Complete setup (first time)** | `./scripts/docker-start.sh` | 3-5 min |
| **Stop services** | `./scripts/docker-stop.sh` | 5 sec |


**Choosing between Local and Docker:**
- Use **Local Development** for faster iteration, easier debugging, and no Docker overhead
- Use **Docker** for production-like environment, consistency across machines, and deployment

## ✨ Features

### Application Features
- 5D neural network interpolation
- Dataset upload (.pkl format)
- Model training with progress tracking
- Single and batch predictions
- RESTful API with OpenAPI documentation
- Modern React-based UI

### Development Features
- Docker containerization
- Hot reload for backend and frontend
- Comprehensive test suite (52 tests)
- 74% code coverage
- API documentation (Swagger UI)
- Environment-based configuration
- Helper scripts for common operations

### Production Features
- Multi-stage Docker builds
- Security hardening (non-root users)
- Health checks
- Persistent volumes
- Backup utilities
- Production deployment scripts

## 🧪 Testing

```bash
# Run all backend tests
./scripts/run_tests.sh test-backend

# Run with coverage
docker-compose exec backend pytest --cov=. --cov-report=html

# View coverage report
open backend/coverage_html/index.html
```

**Test Coverage:** 74.54%
- 28 unit tests (neural network, data handling)
- 24 integration tests (API endpoints)

## 🐳 Docker Architecture

### Services
- **Backend:** Python 3.12 + FastAPI (port 8000)
- **Frontend:** Node 20 + Next.js 16 (port 3000)

### Networks
- Isolated bridge network for inter-service communication

### Volumes
- `interpolator-backend-uploads` - Persistent dataset storage
- `interpolator-backend-data` - Model storage

## 📊 Technology Stack

### Backend
- **Framework:** FastAPI
- **ML Library:** scikit-learn (MLPRegressor)
- **Python:** 3.12
- **Testing:** pytest, pytest-cov
- **Server:** uvicorn

### Frontend
- **Framework:** Next.js 16
- **UI Library:** React 19
- **Styling:** Tailwind CSS v4
- **Language:** TypeScript 5

### Infrastructure
- **Containerization:** Docker
- **Orchestration:** Docker Compose
- **CI/CD Ready:** Multi-stage builds

## 🔒 Environment Variables

Copy and configure environment files:

```bash
# Development
cp .env.development .env

# Production
cp .env.production .env
```

**Key variables:**
- `BACKEND_PORT` - Backend port (default: 8000)
- `FRONTEND_PORT` - Frontend port (default: 3000)
- `NEXT_PUBLIC_API_URL` - API URL for frontend
- `CORS_ORIGINS` - Allowed CORS origins
- `BUILD_TARGET` - Docker build stage (development/production)

See [.env.example](.env.example) for all variables.

## 🚢 Production Deployment

```bash
# 1. Configure production
cp .env.production .env
# Edit with your domain settings

```

## 🛠️ Development Workflow

### Local Development (Recommended)

1. **Start:** `./scripts/local-build.sh`
2. **Code:** Edit files (auto-reload enabled)
3. **View Logs:** Automatically shown, or check `logs/` directory
4. **Stop:** Press `Ctrl+C` or use `./scripts/local-build.sh`

### Docker Development

1. **Start:** `./scripts/docker-start.sh`
2. **Code:** Edit files (auto-reload enabled)
3. **Stop:** `./scripts/docker-stop.sh`

## 📝 API Endpoints

### Health & Status
- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /status` - System status

### Dataset Management
- `POST /upload-fit-dataset/` - Upload training dataset
- `POST /upload-predict-dataset/` - Upload prediction dataset (used for developpement tests)

### Model Operations
- `POST /start-training/` - Train model
- `POST /start-predict/` - Batch prediction
- `POST /predict-single/` - Single prediction

Full API documentation: http://localhost:8000/docs

## 🤝 Use of LLM

Major part of the frontend, the documentation and the tests were developed using Anthropic AI's Claude's Code. 

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 👤 Author

Makimona Kiakisolako (bamk3)
University of Cambridge - DIS Course

## 📞 Support

- **Issues:** email bamk3@cam.ac.uk

---

**Done as coursework of the C1 DIS course at Cambridge**
