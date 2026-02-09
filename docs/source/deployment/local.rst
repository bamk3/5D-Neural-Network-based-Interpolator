Local Deployment Guide
======================

Complete guide for deploying the 5D Interpolator on your local machine.

Quick Deploy Script
-------------------

A comprehensive deployment script is provided for one-command setup:

.. code-block:: bash

   # Make executable
   chmod +x scripts/deploy-local.sh

   # Run deployment
   ./scripts/deploy-local.sh

This script will:

1. Check all prerequisites
2. Set up environment configuration
3. Start backend and frontend services
4. Verify deployment
5. Display access URLs

Manual Deployment Steps
-----------------------

If you prefer manual deployment or need to troubleshoot:

Step 1: Prerequisites Check
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Verify Python:**

.. code-block:: bash

   python3 --version  # Should be 3.12+

**Verify Node.js:**

.. code-block:: bash

   node --version  # Should be 20+
   npm --version   # Should be 10.8+

**Install Missing Dependencies:**

.. code-block:: bash

   # macOS
   brew install python@3.12 node

   # Ubuntu/Debian
   sudo apt install python3.12 nodejs npm

Step 2: Backend Setup
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   cd backend

   # Create virtual environment
   python3 -m venv venv

   # Activate virtual environment
   source venv/bin/activate  # macOS/Linux
   # Or on Windows:
   # venv\Scripts\activate

   # Install dependencies
   pip install --upgrade pip
   pip install -r requirements.txt

   # Verify installation
   python -c "import fastapi; import sklearn; print('Backend ready!')"

Step 3: Frontend Setup
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   cd frontend

   # Install dependencies
   npm install

   # Verify installation
   npm run build  # Should complete without errors

Step 4: Start Services
~~~~~~~~~~~~~~~~~~~~~~

**Terminal 1 - Backend:**

.. code-block:: bash

   cd backend
   source venv/bin/activate
   uvicorn main:app --reload --host 0.0.0.0 --port 8000

Expected output:

.. code-block:: text

   INFO:     Uvicorn running on http://0.0.0.0:8000
   INFO:     Application startup complete.

**Terminal 2 - Frontend:**

.. code-block:: bash

   cd frontend
   npm run dev

Expected output:

.. code-block:: text

   ▲ Next.js 16.0.3
   - Local:        http://localhost:3000
   - Ready in 2.1s

Step 5: Verify Deployment
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Test backend
   curl http://localhost:8000/health

   # Expected: {"status":"healthy","service":"5D Interpolator Backend by bamk3"}

   # Test frontend
   curl -I http://localhost:3000

   # Expected: HTTP/1.1 200 OK

Access the Application
----------------------

Once deployed, access at:

* **Main Application**: http://localhost:3000
* **API Documentation**: http://localhost:8000/docs
* **Alternative API Docs**: http://localhost:8000/redoc

Using the Application
--------------------

Upload Sample Dataset
~~~~~~~~~~~~~~~~~~~~~

A sample dataset is provided for testing. Create it:

.. code-block:: python

   import numpy as np
   import pickle

   # Generate sample data
   np.random.seed(42)
   n_samples = 1000

   # 5D input features
   X = np.random.randn(n_samples, 5)

   # Target: sum of squares with noise
   y = np.sum(X**2, axis=1) + 0.1 * np.random.randn(n_samples)

   # Save training data
   with open('sample_training.pkl', 'wb') as f:
       pickle.dump({'X': X, 'y': y}, f)

   # Save prediction data
   X_pred = np.random.randn(100, 5)
   with open('sample_prediction.pkl', 'wb') as f:
       pickle.dump(X_pred, f)

Upload via UI:

1. Navigate to http://localhost:3000/upload
2. Select "Training" type
3. Upload ``sample_training.pkl``
4. Proceed to training

Environment Configuration
-------------------------

Create ``.env`` file in project root:

.. code-block:: bash

   # Copy from template
   cp .env.development .env

Key variables:

.. code-block:: bash

   # Backend
   BACKEND_PORT=8000
   CORS_ORIGINS=http://localhost:3000

   # Frontend
   FRONTEND_PORT=3000
   NEXT_PUBLIC_API_URL=http://localhost:8000

   # Development
   DEBUG=true
   LOG_LEVEL=INFO

Managing Services
-----------------

Stop Services
~~~~~~~~~~~~~

.. code-block:: bash

   # Press Ctrl+C in each terminal running the services

Restart Services
~~~~~~~~~~~~~~~

.. code-block:: bash

   # Backend
   cd backend
   source venv/bin/activate
   uvicorn main:app --reload

   # Frontend
   cd frontend
   npm run dev

Check Running Services
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Check what's using port 8000
   lsof -i :8000

   # Check what's using port 3000
   lsof -i :3000

Kill Services
~~~~~~~~~~~~~

.. code-block:: bash

   # Kill process on port 8000
   lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

   # Kill process on port 3000
   lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9

Troubleshooting
---------------

Port Already in Use
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Option 1: Kill the process
   lsof -i :8000
   kill -9 <PID>

   # Option 2: Use different port
   # Backend:
   uvicorn main:app --reload --port 8001

   # Frontend: Edit package.json
   "dev": "next dev -p 3001"

Module Not Found Errors
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Backend
   cd backend
   source venv/bin/activate
   pip install -r requirements.txt

   # Frontend
   cd frontend
   rm -rf node_modules package-lock.json
   npm install

Permission Errors
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Python venv creation fails
   sudo chown -R $USER:$USER .

   # npm install fails
   npm cache clean --force
   rm -rf node_modules
   npm install

Database/State Issues
~~~~~~~~~~~~~~~~~~~~

The application uses in-memory state. To reset:

.. code-block:: bash

   # Stop services
   # Delete uploaded files
   rm -rf backend/uploaded_datasets/*

   # Restart services

Performance Optimization
-----------------------

Backend Optimization
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Use production server (gunicorn)
   pip install gunicorn
   gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

Frontend Optimization
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Build for production
   cd frontend
   npm run build
   npm start  # Runs optimized production build

Data Persistence
----------------

Uploaded datasets are stored in:

.. code-block:: text

   backend/
   └── uploaded_datasets/
       ├── training_dataset.pkl
       └── prediction_dataset.pkl

Backup and restore:

.. code-block:: bash

   # Backup
   tar -czf datasets_backup.tar.gz backend/uploaded_datasets/

   # Restore
   tar -xzf datasets_backup.tar.gz

Development Mode Features
-------------------------

Hot Reload
~~~~~~~~~~

Both backend and frontend support hot reload:

* **Backend**: Changes to Python files trigger automatic reload
* **Frontend**: Changes to React components update instantly

Debug Mode
~~~~~~~~~~

.. code-block:: bash

   # Backend with debug logging
   LOG_LEVEL=DEBUG uvicorn main:app --reload

   # Frontend with debug
   npm run dev  # Already in debug mode

API Testing
~~~~~~~~~~~

Use the interactive API docs:

* http://localhost:8000/docs (Swagger UI)
* Test endpoints directly in browser
* View request/response schemas

Next Steps
----------

* :doc:`docker` - Deploy using Docker
* :doc:`production` - Production deployment guide
* :doc:`../testing/overview` - Run test suite
* :doc:`../quickstart` - Application usage guide
