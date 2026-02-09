System Architecture
===================

Comprehensive overview of the 5D Interpolator system architecture.

Overview
--------

The system follows a modern client-server architecture with clear separation of concerns:

.. code-block:: text

   ┌─────────────────────────────────────────────────────┐
   │                    Client Layer                     │
   │  ┌───────────────────────────────────────────────┐  │
   │  │         Next.js Frontend (Port 3000)          │  │
   │  │  - React 19 with TypeScript                   │  │
   │  │  - Tailwind CSS v4                           │  │
   │  │  - Upload/Train/Predict Pages                │  │
   │  └───────────────────────────────────────────────┘  │
   └─────────────────────────────────────────────────────┘
                            │
                            ├─ HTTP REST API
                            │
   ┌─────────────────────────────────────────────────────┐
   │                    Server Layer                     │
   │  ┌───────────────────────────────────────────────┐  │
   │  │        FastAPI Backend (Port 8000)            │  │
   │  │  - RESTful API Endpoints                      │  │
   │  │  - File Upload Handling                       │  │
   │  │  - State Management                           │  │
   │  └───────────────────────────────────────────────┘  │
   └─────────────────────────────────────────────────────┘
                            │
                            ├─ Python Interface
                            │
   ┌─────────────────────────────────────────────────────┐
   │                  Processing Layer                   │
   │  ┌───────────────────────────────────────────────┐  │
   │  │       fivedreg Neural Network Package         │  │
   │  │  - FastNeuralNetwork Class                    │  │
   │  │  - Data Preprocessing                         │  │
   │  │  - Model Training & Prediction                │  │
   │  └───────────────────────────────────────────────┘  │
   └─────────────────────────────────────────────────────┘
                            │
                            ├─ NumPy/sklearn
                            │
   ┌─────────────────────────────────────────────────────┐
   │                  ML Framework Layer                 │
   │  ┌───────────────────────────────────────────────┐  │
   │  │            scikit-learn MLPRegressor          │  │
   │  │  - Neural Network Implementation              │  │
   │  │  - Optimization Algorithms                    │  │
   │  │  - Metrics Calculation                        │  │
   │  └───────────────────────────────────────────────┘  │
   └─────────────────────────────────────────────────────┘

Technology Stack
----------------

Frontend
~~~~~~~~

**Framework & Runtime:**

* Next.js 16.0.3 (React framework)
* React 19.2.0 (UI library)
* Node.js 20+ (runtime)

**Language & Tooling:**

* TypeScript 5 (type safety)
* ESLint (linting)
* Turbopack (build tool)

**Styling:**

* Tailwind CSS v4 (utility-first CSS)
* PostCSS (CSS processing)
* Geist fonts (typography)

**Development:**

* Hot module replacement
* Fast refresh
* TypeScript checking

Backend
~~~~~~~

**Framework:**

* FastAPI 0.115.6 (web framework)
* Uvicorn (ASGI server)
* Python 3.12+

**Core Libraries:**

* NumPy 1.26.4 (numerical computing)
* scikit-learn 1.5.1 (machine learning)
* Pydantic 2.10.5 (validation)

**Testing:**

* pytest 8.3.4 (test framework)
* pytest-cov (coverage reporting)
* pytest-asyncio (async testing)

**Deployment:**

* Docker (containerization)
* Docker Compose (orchestration)

Data Flow
---------

Training Workflow
~~~~~~~~~~~~~~~~~

.. code-block:: text

   1. User selects .pkl file
      ↓
   2. Frontend: POST /upload-fit-dataset/
      ↓
   3. Backend: Save to uploaded_datasets/
      ↓
   4. Backend: Validate format
      ↓
   5. Backend: Return dataset preview
      ↓
   6. Frontend: Display preview
      ↓
   7. User configures hyperparameters
      ↓
   8. Frontend: POST /start-training/
      ↓
   9. Backend: Load dataset
      ↓
   10. Backend: Call benchmark_training_speed()
      ↓
   11. fivedreg: Preprocess data
      ↓
   12. fivedreg: Train FastNeuralNetwork
      ↓
   13. fivedreg: Calculate metrics
      ↓
   14. Backend: Store model in memory
      ↓
   15. Backend: Return metrics
      ↓
   16. Frontend: Display results

Prediction Workflow
~~~~~~~~~~~~~~~~~~~

**Batch Prediction:**

.. code-block:: text

   1. User selects .pkl file
      ↓
   2. Frontend: POST /upload-predict-dataset/
      ↓
   3. Backend: Save file
      ↓
   4. Backend: Validate format
      ↓
   5. Frontend: POST /start-predict/
      ↓
   6. Backend: Load dataset
      ↓
   7. Backend: Use stored model
      ↓
   8. fivedreg: Generate predictions
      ↓
   9. Backend: Return predictions
      ↓
   10. Frontend: Display results

**Single Prediction:**

.. code-block:: text

   1. User enters 5 feature values
      ↓
   2. Frontend: POST /predict-single/
      ↓
   3. Backend: Validate input
      ↓
   4. Backend: Use stored model
      ↓
   5. fivedreg: Predict single value
      ↓
   6. Backend: Return prediction
      ↓
   7. Frontend: Display result

State Management
----------------

Backend State
~~~~~~~~~~~~~

The backend maintains global state:

.. code-block:: python

   # Global variables in main.py
   processing_result = None      # Path to training dataset
   train_result = None           # (model, metrics) tuple
   predict_input = None          # Path to prediction dataset
   model = None                  # Trained FastNeuralNetwork

**State Lifecycle:**

1. ``processing_result`` set on training upload
2. ``train_result`` and ``model`` set on training completion
3. ``predict_input`` set on prediction upload
4. ``model`` used for all predictions
5. State cleared on server restart

**Implications:**

* Server must stay running between operations
* No concurrent users (single session)
* State lost on crash/restart
* Suitable for development/coursework

Frontend State
~~~~~~~~~~~~~~

Each page manages its own state using React hooks:

.. code-block:: typescript

   // Upload page
   const [file, setFile] = useState<File | null>(null)
   const [uploadResult, setUploadResult] = useState<any>(null)

   // Train page
   const [trainingDataUploaded, setTrainingDataUploaded] = useState(false)
   const [modelTrained, setModelTrained] = useState(false)
   const [trainResult, setTrainResult] = useState<any>(null)
   const [hyperparameters, setHyperparameters] = useState({...})

   // Predict page
   const [predictionMode, setPredictionMode] = useState<'batch' | 'single'>('batch')
   const [predictionResult, setPredictionResult] = useState<any>(null)
   const [singlePrediction, setSinglePrediction] = useState<number | null>(null)

**State Synchronization:**

* Polls ``/status`` endpoint on mount
* Updates local state based on server state
* Enables/disables UI based on state

API Design
----------

RESTful Principles
~~~~~~~~~~~~~~~~~~

The API follows REST conventions:

* ``GET`` for retrieving state
* ``POST`` for creating/triggering operations
* JSON request/response bodies
* HTTP status codes for errors
* CORS enabled for development

Endpoints
~~~~~~~~~

**Health & Status:**

.. code-block:: text

   GET  /           → Welcome message
   GET  /health     → Health check
   GET  /status     → System state

**Upload:**

.. code-block:: text

   POST /upload-fit-dataset/      → Upload training data
   POST /upload-predict-dataset/  → Upload prediction data

**Training:**

.. code-block:: text

   POST /start-training/  → Train model with hyperparameters

**Prediction:**

.. code-block:: text

   POST /start-predict/   → Batch prediction
   POST /predict-single/  → Single prediction

Request/Response Format
~~~~~~~~~~~~~~~~~~~~~~~

**Training Request:**

.. code-block:: json

   {
     "hyperparameters": {
       "hidden_layer_1": 128,
       "hidden_layer_2": 64,
       "hidden_layer_3": 32,
       "learning_rate": 0.001,
       "max_iterations": 500,
       "early_stopping": true
     }
   }

**Training Response:**

.. code-block:: json

   {
     "status": "success",
     "metrics": {
       "r2_score": 0.9872,
       "mse": 0.0123,
       "mae": 0.0891,
       "rmse": 0.1109,
       "training_time": 23.45
     },
     "hyperparameters": {
       "hidden_layer_1": 128,
       "hidden_layer_2": 64,
       "hidden_layer_3": 32,
       "learning_rate": 0.001,
       "max_iterations": 500,
       "early_stopping": true
     }
   }

**Prediction Response:**

.. code-block:: json

   {
     "predictions": [1.234, 5.678, ...],
     "count": 100
   }

Data Processing Pipeline
------------------------

Data Validation
~~~~~~~~~~~~~~~

**Step 1: File Format Validation**

.. code-block:: python

   # Check file extension
   if not filename.endswith('.pkl'):
       raise ValueError("File must be .pkl format")

   # Try to load pickle
   try:
       data = pickle.load(file)
   except Exception:
       raise ValueError("Invalid pickle file")

**Step 2: Structure Validation**

.. code-block:: python

   # Training data
   if not isinstance(data, dict):
       raise ValueError("Must be dictionary")

   if 'X' not in data or 'y' not in data:
       raise ValueError("Must contain 'X' and 'y'")

   # Prediction data
   if not isinstance(data, np.ndarray):
       raise ValueError("Must be NumPy array")

**Step 3: Shape Validation**

.. code-block:: python

   # Check dimensions
   if data['X'].shape[1] != 5:
       raise ValueError("X must have 5 features")

   if data['y'].ndim != 1:
       raise ValueError("y must be 1D")

   if data['X'].shape[0] != data['y'].shape[0]:
       raise ValueError("X and y must have same samples")

**Step 4: Value Validation**

.. code-block:: python

   # Check for invalid values
   if np.any(np.isnan(data['X'])) or np.any(np.isinf(data['X'])):
       raise ValueError("X contains NaN or inf")

   if np.any(np.isnan(data['y'])) or np.any(np.isinf(data['y'])):
       raise ValueError("y contains NaN or inf")

Data Preprocessing
~~~~~~~~~~~~~~~~~~

**Step 1: Clean Data**

.. code-block:: python

   # Remove NaN rows
   mask = ~(np.isnan(X).any(axis=1) | np.isnan(y))
   X = X[mask]
   y = y[mask]

**Step 2: Split Data**

.. code-block:: python

   # 60% train, 20% validation, 20% test
   X_temp, X_test, y_temp, y_test = train_test_split(
       X, y, test_size=0.2, random_state=42
   )

   X_train, X_val, y_train, y_val = train_test_split(
       X_temp, y_temp, test_size=0.25, random_state=42
   )

**Step 3: Standardize**

.. code-block:: python

   scaler = StandardScaler()
   X_train = scaler.fit_transform(X_train)
   X_val = scaler.transform(X_val)
   X_test = scaler.transform(X_test)

Security Considerations
-----------------------

Current Implementation
~~~~~~~~~~~~~~~~~~~~~~

**Suitable for:**

* Local development
* Coursework/academic use
* Single-user scenarios

**Not suitable for:**

* Production deployment
* Multi-user systems
* Public internet exposure

Security Measures
~~~~~~~~~~~~~~~~~

**Input Validation:**

* File size limits
* Format validation
* Value range checking
* Type validation with Pydantic

**CORS Configuration:**

.. code-block:: python

   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:3000"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )

**For Production:**

Would need:

* Authentication & authorization
* Rate limiting
* File scanning
* HTTPS/TLS
* Database for state
* Session management
* Input sanitization
* Error message sanitization

Scalability
-----------

Current Limitations
~~~~~~~~~~~~~~~~~~~

* Single server instance
* In-memory state
* No horizontal scaling
* No load balancing
* Limited to CPU training

Potential Improvements
~~~~~~~~~~~~~~~~~~~~~~

**For Higher Scale:**

1. **Database Integration:**

   * Store models in database
   * Persist training state
   * Support multiple users

2. **Queue System:**

   * Background job processing
   * Async training tasks
   * Progress tracking

3. **Caching:**

   * Redis for session state
   * Model caching
   * Result caching

4. **Microservices:**

   * Separate training service
   * Separate prediction service
   * API gateway

5. **GPU Support:**

   * PyTorch/TensorFlow
   * CUDA acceleration
   * Larger networks

Deployment Options
------------------

Development
~~~~~~~~~~~

**Local:**

.. code-block:: bash

   ./scripts/deploy-local.sh

**Docker:**

.. code-block:: bash

   docker compose up

Production
~~~~~~~~~~

**Cloud Platforms:**

* AWS (ECS, Lambda, SageMaker)
* Google Cloud (Cloud Run, AI Platform)
* Azure (App Service, ML)

**Containerization:**

* Docker images
* Kubernetes orchestration
* Auto-scaling

Monitoring & Logging
--------------------

Current Logging
~~~~~~~~~~~~~~~

**Backend:**

* Uvicorn access logs
* Python print statements
* Error stack traces

**Frontend:**

* Console.log debugging
* Error boundaries

Production Logging
~~~~~~~~~~~~~~~~~~

Would need:

* Structured logging (JSON)
* Log aggregation (ELK stack)
* Error tracking (Sentry)
* Performance monitoring (APM)
* User analytics

Testing Strategy
----------------

**Unit Tests:**

* Backend endpoints (pytest)
* Neural network module
* Data handlers
* Validation logic

**Integration Tests:**

* End-to-end workflows
* API contract testing
* Database interactions

**Coverage:**

* 74.54% overall
* 52 total tests

See :doc:`testing/overview` for details.

Next Steps
----------

* :doc:`deployment/local` - Local deployment guide
* :doc:`deployment/docker` - Docker deployment
* :doc:`api/backend` - Backend API reference
* :doc:`testing/overview` - Testing documentation
