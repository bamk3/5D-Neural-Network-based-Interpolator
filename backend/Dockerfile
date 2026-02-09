# Multi-stage Dockerfile for 5D Interpolator Backend
# Optimized for production deployment with minimal image size

# =============================================================================
# Stage 1: Base Image with Python Dependencies
# =============================================================================
FROM python:3.12-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# =============================================================================
# Stage 2: Development Image
# =============================================================================
FROM base as development

# Copy requirements
COPY requirements.txt requirements-dev.txt ./

# Install all dependencies (including dev dependencies)
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-dev.txt

# Copy application code
COPY . .

# Install the fivedreg package in editable mode
RUN pip install -e .

# Create directories for uploads and data
RUN mkdir -p uploaded_datasets data

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Run development server with auto-reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# =============================================================================
# Stage 3: Production Image (Optimized)
# =============================================================================
FROM base as production

# Copy requirements (production only)
COPY requirements.txt ./

# Install production dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the fivedreg package
RUN pip install --no-cache-dir .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    mkdir -p uploaded_datasets data && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Run production server with gunicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

# =============================================================================
# Stage 4: Testing Image
# =============================================================================
FROM development as testing

# Run tests
RUN pytest tests/ -v --cov=. --cov-report=term-missing

# Default to development stage if not specified
FROM development
