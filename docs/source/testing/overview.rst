Testing Overview
================

The 5D Interpolator includes a comprehensive test suite ensuring reliability and correctness.

Test Suite Summary
------------------

**Total Tests**: 52
**Code Coverage**: 74.54%
**Testing Framework**: pytest
**Coverage Tool**: pytest-cov

Test Categories
---------------

The test suite is organized into two main categories:

Unit Tests (28 tests)
~~~~~~~~~~~~~~~~~~~~~

Located in ``backend/tests/unit/``

**test_neural_network.py** (17 tests)

Tests for the ``FastNeuralNetwork`` class:

* Initialization with various configurations
* Model fitting and training
* Prediction functionality
* Performance evaluation metrics
* Hyperparameter configurations
* Error handling

**test_data_handler.py** (11 tests)

Tests for data loading and preprocessing:

* Dataset loading from files
* Train/validation/test splitting
* Data standardization
* NaN/invalid value handling
* Input validation

Integration Tests (24 tests)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Located in ``backend/tests/integration/``

**test_api_endpoints.py** (24 tests)

End-to-end API testing:

* Health check endpoints
* Dataset upload workflows
* Training workflows with various hyperparameters
* Prediction workflows (batch and single)
* Error handling and edge cases
* Complete end-to-end workflows

Running Tests
-------------

Using Docker
~~~~~~~~~~~

.. code-block:: bash

   # Run all tests
   ./scripts/docker-dev.sh test-backend

   # Run with coverage report
   docker compose exec backend pytest --cov=. --cov-report=html

   # Run specific test file
   docker compose exec backend pytest tests/unit/test_neural_network.py

   # Run with verbose output
   docker compose exec backend pytest -v

Manual Installation
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   cd backend

   # Activate virtual environment (if using one)
   source venv/bin/activate

   # Run all tests
   pytest

   # Run with coverage
   pytest --cov=. --cov-report=html --cov-report=term

   # Run specific tests
   pytest tests/unit/
   pytest tests/integration/

   # Run with markers
   pytest -m "not slow"

Test Configuration
------------------

pytest.ini
~~~~~~~~~~

Located at ``backend/pytest.ini``:

.. code-block:: ini

   [pytest]
   testpaths = tests
   python_files = test_*.py
   python_classes = Test*
   python_functions = test_*
   addopts = -v --tb=short --strict-markers
   markers =
       unit: Unit tests
       integration: Integration tests
       slow: Slow running tests

   [coverage:run]
   source = .
   omit =
       */tests/*
       */venv/*
       */__pycache__/*
       */site-packages/*

   [coverage:report]
   precision = 2
   show_missing = True
   skip_covered = False

Test Fixtures
-------------

Shared fixtures are defined in ``backend/tests/conftest.py``:

sample_data_small
~~~~~~~~~~~~~~~~~

Generates small dataset (100 samples) for quick tests.

.. code-block:: python

   @pytest.fixture
   def sample_data_small():
       """Generate small sample data for testing"""
       np.random.seed(42)
       X = np.random.randn(100, 5)
       y = np.sum(X**2, axis=1)
       return X, y

sample_data_medium
~~~~~~~~~~~~~~~~~~

Generates medium dataset (1000 samples) for realistic tests.

.. code-block:: python

   @pytest.fixture
   def sample_data_medium():
       """Generate medium sample data for testing"""
       np.random.seed(42)
       X = np.random.randn(1000, 5)
       y = np.sum(X**2, axis=1)
       return X, y

temp_dataset_file
~~~~~~~~~~~~~~~~~

Creates temporary dataset file for upload tests.

.. code-block:: python

   @pytest.fixture
   def temp_dataset_file(tmp_path, sample_data_small):
       """Create temporary dataset file"""
       X, y = sample_data_small
       data = {'X': X, 'y': y}
       filepath = tmp_path / "test_dataset.pkl"
       with open(filepath, 'wb') as f:
           pickle.dump(data, f)
       return filepath

test_client
~~~~~~~~~~~

FastAPI test client for API integration tests.

.. code-block:: python

   @pytest.fixture
   def test_client():
       """Create FastAPI test client"""
       from main import app
       return TestClient(app)

reset_global_state
~~~~~~~~~~~~~~~~~~

Resets global state between tests.

.. code-block:: python

   @pytest.fixture(autouse=True)
   def reset_global_state():
       """Reset global state before each test"""
       import main
       main.processing_result = None
       main.train_result = None
       main.predict_input = None
       yield
       # Cleanup after test

Coverage Report
--------------

Current Coverage by Module
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Module                              Statements    Missing    Coverage
   ─────────────────────────────────────────────────────────────────────
   main.py                                    198         30      84.85%
   fivedreg/base_fivedreg.py                  106         15      85.85%
   fivedreg/data_hand/module.py                45          5      88.89%
   fivedreg/__init__.py                         3          0     100.00%
   ─────────────────────────────────────────────────────────────────────
   TOTAL                                      352         50      74.54%

Viewing Coverage Reports
~~~~~~~~~~~~~~~~~~~~~~~~

**HTML Report:**

.. code-block:: bash

   # Generate HTML coverage report
   pytest --cov=. --cov-report=html

   # Open in browser
   open backend/htmlcov/index.html  # macOS
   xdg-open backend/htmlcov/index.html  # Linux

**Terminal Report:**

.. code-block:: bash

   pytest --cov=. --cov-report=term-missing

Example Test Cases
------------------

Unit Test Example
~~~~~~~~~~~~~~~~

.. code-block:: python

   def test_neural_network_initialization():
       """Test that neural network initializes with correct defaults"""
       model = FastNeuralNetwork()

       assert model.hidden_layers == (64, 32, 16)
       assert model.learning_rate == 0.001
       assert model.max_iterations == 500
       assert model.early_stopping == True

Integration Test Example
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def test_complete_workflow(test_client, temp_dataset_file):
       """Test complete workflow: upload -> train -> predict"""

       # Upload training dataset
       with open(temp_dataset_file, 'rb') as f:
           response = test_client.post(
               "/upload-fit-dataset/",
               files={"file": ("test.pkl", f, "application/octet-stream")}
           )
       assert response.status_code == 200

       # Train model
       response = test_client.post(
           "/start-training/",
           json={"hyperparameters": {"max_iterations": 100}}
       )
       assert response.status_code == 200
       result = response.json()
       assert "function_result" in result
       assert result["function_result"]["r2"] > 0.5

       # Single prediction
       response = test_client.post(
           "/predict-single/",
           json={"features": [1.0, 2.0, 3.0, 4.0, 5.0]}
       )
       assert response.status_code == 200
       assert "prediction" in response.json()

Continuous Integration
----------------------

The test suite is designed to run in CI/CD pipelines:

GitHub Actions Example
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   name: Tests
   on: [push, pull_request]

   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - name: Set up Python
           uses: actions/setup-python@v2
           with:
             python-version: '3.12'
         - name: Install dependencies
           run: |
             cd backend
             pip install -r requirements.txt
             pip install -r requirements-dev.txt
         - name: Run tests
           run: |
             cd backend
             pytest --cov=. --cov-report=xml
         - name: Upload coverage
           uses: codecov/codecov-action@v2

Writing New Tests
-----------------

Guidelines
~~~~~~~~~~

1. **Test Naming**: Use descriptive names starting with ``test_``
2. **One Assertion Per Test**: Keep tests focused
3. **Use Fixtures**: Leverage shared fixtures for setup
4. **Test Edge Cases**: Include boundary conditions
5. **Mock External Dependencies**: Use mocks for external services

Example New Test
~~~~~~~~~~~~~~~

.. code-block:: python

   import pytest
   from fivedreg import FastNeuralNetwork

   def test_custom_architecture():
       """Test neural network with custom architecture"""
       # Arrange
       custom_layers = (128, 64, 32)
       model = FastNeuralNetwork(hidden_layers=custom_layers)

       # Act
       params = model.get_params()

       # Assert
       assert params['hidden_layers'] == custom_layers

Performance Tests
-----------------

Training Speed Test
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time

   def test_training_speed(sample_data_medium):
       """Test that training completes within time limit"""
       X, y = sample_data_medium
       model = FastNeuralNetwork(max_iterations=500)

       start = time.time()
       model.fit(X, y)
       elapsed = time.time() - start

       assert elapsed < 60, f"Training took {elapsed:.2f}s (limit: 60s)"

Troubleshooting Tests
---------------------

Common Issues
~~~~~~~~~~~~~

**ImportError: No module named 'main'**

.. code-block:: bash

   # Ensure you're in backend directory
   cd backend
   pytest

**Coverage data not found**

.. code-block:: bash

   # Delete old coverage data
   rm .coverage
   pytest --cov=.

**Tests hang or timeout**

.. code-block:: bash

   # Reduce iterations in tests
   # Check for infinite loops

Next Steps
----------

* :doc:`coverage` - Detailed coverage analysis
* :doc:`../api/backend` - API testing reference
* :doc:`../deployment/local` - Local testing setup
