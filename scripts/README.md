# Scripts Directory

This directory contains all helper scripts for the 5D Interpolator project.

## Available Scripts

### 🏠 Local Development (No Docker)

**`local-build.sh`** - Complete local setup and launch
```bash
./scripts/local-build.sh
```

This script performs:
1. **Check Prerequisites** - Verifies Python 3, Node.js, npm, and pip3 are installed
2. **Backend Setup** - Creates virtual environment, installs dependencies
3. **Frontend Setup** - Installs npm dependencies
4. **Launch Services** - Starts both backend and frontend servers
5. **Display Logs** - Shows real-time logs from both services

**When to use:**
- Local development without Docker
- Faster iteration and debugging
- When Docker is not available
- Testing on native environment

**Prerequisites:**
- Python 3.8 or higher
- Node.js 18 or higher
- pip3 and npm

**Stop services:** Press `Ctrl+C` or run `./scripts/local-stop.sh`

**Logs location:**
- Backend: `logs/backend.log`
- Frontend: `logs/frontend.log`

**`local-stop.sh`** - Stop local services
```bash
./scripts/local-stop.sh
```

This script performs:
1. **Read PID File** - Finds all processes started by `local-build.sh`
2. **Kill Processes** - Gracefully stops backend and frontend processes
3. **Port Cleanup** - Finds and kills any processes using ports 8000 and 3000
4. **Verification** - Confirms ports are free and services are stopped
5. **Cleanup** - Removes PID tracking files

**What it does:**
- Stops all processes tracked in `.local-build-pids`
- Finds and stops processes on backend port (8000)
- Finds and stops processes on frontend port (3000)
- Attempts graceful shutdown (SIGTERM) first, then force kill (SIGKILL) if needed
- Verifies all ports are free
- Provides detailed status for each stopped process

**What it preserves:**
- Python virtual environment (`backend/venv/`)
- Node modules (`frontend/node_modules/`)
- Uploaded datasets
- Log files

**When to use:**
- After using `local-build.sh` and you want to stop services
- When processes are stuck and ports are blocked
- Before starting Docker to free up ports
- When you see "port already in use" errors

### 🐳 Docker Scripts

**`docker-start.sh`** - Complete setup (clean + rebuild + start)
```bash
./scripts/docker-start.sh
```

This script performs:
1. **Clean** - Removes all containers, networks, and volumes
2. **Rebuild** - Builds Docker images from scratch (no cache)
3. **Start** - Starts all services

**When to use:**
- First time setup
- After major code changes
- When experiencing Docker issues
- Fresh start needed

**`docker-stop.sh`** - Stop all services
```bash
./scripts/docker-stop.sh
```

This script:
- Gracefully stops all running services
- Shows current status before stopping
- Asks for confirmation
- Preserves volumes (data not deleted)

**When to use:**
- End of work session
- Before system shutdown
- To free up resources

### 💻 Development Scripts

**`docker-dev.sh`** - Development helper
```bash
./scripts/docker-dev.sh [command]
```

**Commands:**
- `start` - Start services in development mode
- `stop` - Stop all services
- `restart` - Restart services
- `build` - Build images (with cache)
- `rebuild` - Rebuild images (no cache)
- `logs` - View all logs
- `logs-backend` - View backend logs
- `logs-frontend` - View frontend logs
- `shell-backend` - Open shell in backend container
- `shell-frontend` - Open shell in frontend container
- `test-backend` - Run backend tests
- `clean` - Remove all containers and volumes
- `status` - Show service status
- `help` - Show help

### 🚢 Production Scripts

**`docker-prod.sh`** - Production deployment helper
```bash
./scripts/docker-prod.sh [command]
```

**Commands:**
- `deploy` - Build and deploy in production
- `start` - Start production services
- `stop` - Stop services
- `restart` - Restart services
- `build` - Build production images
- `logs` - View logs
- `status` - Show status
- `health` - Check service health
- `backup` - Backup volumes
- `help` - Show help

## Quick Reference

### First Time Setup

**Local Development (Recommended):**
```bash
# One command to install and launch everything
./scripts/local-build.sh
```

**Docker:**
```bash
# Complete setup from scratch
./scripts/docker-start.sh
```

### Daily Development

**Local Development:**
```bash
# Start working
./scripts/local-build.sh

# View logs (automatically shown, or check separately)
tail -f logs/backend.log
tail -f logs/frontend.log

# Stop when done
# Press Ctrl+C or:
./scripts/local-stop.sh
```

**Docker:**
```bash
# Start working
./scripts/docker-dev.sh start

# View logs while coding
./scripts/docker-dev.sh logs

# Run tests
./scripts/docker-dev.sh test-backend

# Stop when done
./scripts/docker-stop.sh
```

### Debugging
```bash
# Check status
./scripts/docker-dev.sh status

# Open backend shell
./scripts/docker-dev.sh shell-backend

# View backend logs
./scripts/docker-dev.sh logs-backend
```

### When Things Break
```bash
# Clean start
./scripts/docker-start.sh

# Or manually:
./scripts/docker-dev.sh clean
./scripts/docker-dev.sh rebuild
./scripts/docker-dev.sh start
```

### Production Deployment
```bash
# Deploy to production
./scripts/docker-prod.sh deploy

# Check health
./scripts/docker-prod.sh health

# Monitor
./scripts/docker-prod.sh logs
```

## Script Locations

All scripts are in the `scripts/` directory. Run them from the project root:

```bash
# From project root
./scripts/docker-start.sh
./scripts/docker-dev.sh start
./scripts/docker-prod.sh deploy
```

## Troubleshooting Scripts

If scripts don't run:

```bash
# Make them executable
chmod +x scripts/*.sh

# Or run with bash
bash scripts/docker-start.sh
```

## Environment Files

Scripts automatically load environment variables from `.env` file in project root.

**Setup environment:**
```bash
# Copy development settings
cp .env.development .env

# Or copy production settings
cp .env.production .env
```

## Getting Help

Each script has a help command:

```bash
./scripts/docker-dev.sh help
./scripts/docker-prod.sh help
```

For more information, see:
- `../DOCKER_README.md` - Complete Docker guide
- `../DOCKER_QUICKSTART.md` - Quick reference
