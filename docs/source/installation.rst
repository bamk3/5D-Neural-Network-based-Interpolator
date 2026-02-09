Installation Guide
==================

This guide covers all methods for installing and running the 5D Neural Network Interpolator.

Prerequisites
-------------

System Requirements
~~~~~~~~~~~~~~~~~~

* **Operating System**: macOS, Linux, or Windows (with WSL2)
* **RAM**: Minimum 4GB (8GB recommended)
* **Disk Space**: Minimum 2GB free space
* **Internet Connection**: Required for initial setup

Software Requirements
~~~~~~~~~~~~~~~~~~~~

**For Docker Installation (Recommended):**

* Docker 20.10+ or Docker Desktop
* Docker Compose v2.0+

**For Manual Installation:**

* Python 3.12+
* Node.js 20+
* npm 10.8+
* pip 23+

Installation Methods
-------------------

Method 1: Docker Installation (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the fastest and most reliable method.

**Step 1: Verify Docker is Running**

.. code-block:: bash

   # Check Docker is installed and running
   docker --version
   docker compose version

   # On Linux, ensure Docker service is running
   sudo systemctl status docker

**Step 2: Clone the Repository**

.. code-block:: bash

   git clone <repository-url>
   cd interpolator

**Step 3: Run Setup Script**

.. code-block:: bash

   # Complete setup (clean + rebuild + start)
   ./scripts/docker-start.sh

This script will:

1. Check if Docker is running
2. Clean up any existing containers
3. Create environment configuration
4. Build Docker images (~3-5 minutes)
5. Start all services
6. Display access URLs

**Step 4: Verify Installation**

.. code-block:: bash

   # Check service status
   docker compose ps

   # Test backend health
   curl http://localhost:8000/health

   # Test frontend (should return HTML)
   curl http://localhost:3000

**Access URLs:**

* Frontend: http://localhost:3000
* Backend API: http://localhost:8000
* API Documentation: http://localhost:8000/docs

Method 2: Manual Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Step 1: Install Backend Dependencies**

.. code-block:: bash

   cd backend

   # Create virtual environment (recommended)
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

**Step 2: Install Frontend Dependencies**

.. code-block:: bash

   cd frontend
   npm install

**Step 3: Start Backend Server**

.. code-block:: bash

   cd backend
   source venv/bin/activate  # If using virtual environment
   uvicorn main:app --reload --host 0.0.0.0 --port 8000

**Step 4: Start Frontend Server** (in new terminal)

.. code-block:: bash

   cd frontend
   npm run dev

**Access URLs:**

* Frontend: http://localhost:3000
* Backend API: http://localhost:8000
* API Documentation: http://localhost:8000/docs

Environment Configuration
------------------------

Environment Variables
~~~~~~~~~~~~~~~~~~~~

The application uses environment variables for configuration. Three preset files are provided:

* ``.env.development`` - For local development
* ``.env.production`` - For production deployment
* ``.env.example`` - Template with all available variables

**Key Variables:**

.. code-block:: bash

   # Backend
   BACKEND_PORT=8000
   CORS_ORIGINS=http://localhost:3000

   # Frontend
   FRONTEND_PORT=3000
   NEXT_PUBLIC_API_URL=http://localhost:8000

   # Docker
   BUILD_TARGET=development  # or 'production'

**Setup:**

.. code-block:: bash

   # Copy development configuration
   cp .env.development .env

   # Or for production
   cp .env.production .env

Troubleshooting
--------------

Docker Issues
~~~~~~~~~~~~

**"Docker is not running" error:**

.. code-block:: bash

   # macOS
   open -a Docker

   # Linux
   sudo systemctl start docker

   # Check status
   docker info

**"Port already in use" error:**

.. code-block:: bash

   # Find process using port 3000
   lsof -i :3000

   # Kill the process
   kill -9 <PID>

**"docker-compose: command not found":**

You have Docker Compose v2 (plugin version). Use:

.. code-block:: bash

   docker compose  # (with space, not hyphen)

Permission Issues (Linux)
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Add user to docker group
   sudo usermod -aG docker $USER

   # Apply changes
   newgrp docker

   # Verify
   docker ps

Python/Node Issues
~~~~~~~~~~~~~~~~~

**Wrong Python version:**

.. code-block:: bash

   # Check version
   python3 --version

   # Install Python 3.12 via package manager
   # macOS:
   brew install python@3.12

   # Ubuntu/Debian:
   sudo apt install python3.12

**npm install fails:**

.. code-block:: bash

   # Clear npm cache
   npm cache clean --force

   # Delete node_modules and retry
   rm -rf node_modules package-lock.json
   npm install

Verifying Installation
---------------------

Run the complete test suite to verify everything works:

.. code-block:: bash

   # Using Docker
   ./scripts/docker-dev.sh test-backend

   # Manual installation
   cd backend
   pytest

Expected output: ``52 passed`` with ``74% coverage``

Building Documentation
----------------------

This documentation can be built locally for offline access:

Quick Build
~~~~~~~~~~~

.. code-block:: bash

   ./scripts/build-docs.sh

This automated script will:

1. Check Python installation (3.12+ required)
2. Create virtual environment for Sphinx
3. Install Sphinx and dependencies
4. Build HTML documentation
5. Open in your default browser

The documentation will be available at:

.. code-block:: text

   docs/build/html/index.html

Manual Build
~~~~~~~~~~~~

For manual control over the build process:

.. code-block:: bash

   cd docs

   # Create virtual environment (first time only)
   python3 -m venv venv
   source venv/bin/activate

   # Install dependencies (first time only)
   pip install -r requirements.txt

   # Build documentation
   sphinx-build -b html source build/html

   # Open in browser
   open build/html/index.html  # macOS
   xdg-open build/html/index.html  # Linux

Rebuilding Documentation
~~~~~~~~~~~~~~~~~~~~~~~~

To rebuild after making changes:

.. code-block:: bash

   cd docs
   source venv/bin/activate

   # Clean previous build
   rm -rf build/html

   # Rebuild
   sphinx-build -b html source build/html

Documentation Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~

The documentation build requires:

* Python 3.12+
* Sphinx 8.2.3+
* sphinx-rtd-theme
* sphinxcontrib packages

All dependencies are listed in ``docs/requirements.txt``

Downloading Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Generate Downloadable Documentation:**

.. code-block:: bash

   ./scripts/build-docs-pdf.sh

This generates multiple downloadable formats:

* **PDF**: ``docs/build/downloads/5D-Interpolator-Documentation.pdf`` (~419 KB)
* **HTML Archive (tar.gz)**: ``docs/build/downloads/5D-Interpolator-Documentation-HTML.tar.gz`` (~8.2 MB)
* **HTML Archive (zip)**: ``docs/build/downloads/5D-Interpolator-Documentation-HTML.zip`` (~8.2 MB)

**PDF Generation Requirements:**

For LaTeX-based PDF (recommended):

* **macOS**: Install MacTeX

  .. code-block:: bash

     brew install --cask mactex

* **Ubuntu/Debian**:

  .. code-block:: bash

     sudo apt-get install texlive-latex-extra texlive-fonts-recommended

* **Fallback**: If LaTeX not available, script automatically uses rst2pdf

**Using Downloaded Documentation:**

* **PDF**: Open directly in any PDF reader
* **HTML Archives**: Extract and open ``index.html`` in a web browser

  .. code-block:: bash

     # Extract tar.gz
     tar -xzf 5D-Interpolator-Documentation-HTML.tar.gz
     open html/index.html

     # Or extract zip
     unzip 5D-Interpolator-Documentation-HTML.zip
     open index.html

Next Steps
----------

* :doc:`quickstart` - Get started with your first model
* :doc:`usage` - Learn about features and workflows
* :doc:`datasets` - Understand dataset requirements
