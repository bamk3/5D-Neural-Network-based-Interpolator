# Testing Suite for 5D Interpolator Backend

This directory contains a comprehensive testing suite for the 5D Interpolator backend application.

## Overview

The test suite validates all system components and ensures reliability through:
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test API endpoints and component interactions
- **Fixtures**: Reusable test data and utilities

## Directory Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # Pytest configuration and shared fixtures
├── README.md                   # This file
├── unit/                       # Unit tests
│   ├── __init__.py
│   ├── test_neural_network.py  # Tests for FastNeuralNetwork class
│   └── test_data_handler.py    # Tests for data loading and preprocessing
├── integration/                # Integration tests
│   ├── __init__.py
│   └── test_api_endpoints.py   # Tests for FastAPI endpoints
└── fixtures/                   # Test fixtures and utilities
    ├── __init__.py
    ├── data_generators.py      # Utilities for generating test data
    └── test_data/              # Pre-generated test datasets
        ├── linear_small.pkl
        ├── linear_medium.pkl
        ├── linear_large.pkl
        ├── nonlinear.pkl
        ├── with_outliers.pkl
        ├── with_missing.pkl
        └── prediction_data.pkl
```

## Installation

Install testing dependencies:

```bash
cd backend
pip install -r requirements-dev.txt
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run with Coverage Report

```bash
pytest --cov=. --cov-report=html
```

This generates an HTML coverage report in `coverage_html/`.

### Run Specific Test Categories

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only fast tests (skip slow tests)
pytest -m "not slow"

# Run only model-related tests
pytest -m model

# Run only API tests
pytest -m api

# Run only data handling tests
pytest -m data
```

### Run Specific Test Files

```bash
# Test neural network module
pytest tests/unit/test_neural_network.py

# Test data handler module
pytest tests/unit/test_data_handler.py

# Test API endpoints
pytest tests/integration/test_api_endpoints.py
```

### Run Specific Test Classes or Functions

```bash
# Run a specific test class
pytest tests/unit/test_neural_network.py::TestFastNeuralNetwork

# Run a specific test function
pytest tests/unit/test_neural_network.py::TestFastNeuralNetwork::test_initialization_default
```

### Run Tests in Parallel

For faster execution on multi-core systems:

```bash
pytest -n auto
```

### Verbose Output

```bash
pytest -v
```

### Stop at First Failure

```bash
pytest -x
```

### Run Last Failed Tests

```bash
pytest --lf
```

## Test Markers

Tests are organized using pytest markers:

- `@pytest.mark.unit` - Unit tests for individual components
- `@pytest.mark.integration` - Integration tests for API endpoints
- `@pytest.mark.slow` - Tests that take longer to run (>1 second)
- `@pytest.mark.fast` - Quick tests (<1 second)
- `@pytest.mark.model` - Tests related to neural network model
- `@pytest.mark.api` - Tests related to API endpoints
- `@pytest.mark.data` - Tests related to data handling

## Available Fixtures

### Data Fixtures

- `sample_data_small` - Small dataset (100 samples)
- `sample_data_medium` - Medium dataset (1000 samples)
- `sample_data_large` - Large dataset (5000 samples)
- `sample_data_with_nans` - Dataset with NaN values for testing cleanup

### File Fixtures

- `temp_dataset_file` - Temporary .pkl file with small dataset
- `temp_dataset_file_medium` - Temporary .pkl file with medium dataset
- `temp_predict_data` - Temporary prediction data file
- `invalid_dataset_file` - Invalid dataset for error testing

### Application Fixtures

- `test_client` - FastAPI TestClient for API testing
- `uploaded_datasets_dir` - Managed upload directory
- `reset_global_state` - Reset global state variables between tests
- `mock_trained_model` - Pre-trained model for testing predictions

## Test Coverage

Current test coverage includes:

### Neural Network Module (`fivedreg.base_fivedreg`)
- ✅ Model initialization (default and custom parameters)
- ✅ Model fitting with valid data
- ✅ Input validation (wrong shapes, mismatched samples)
- ✅ Prediction functionality
- ✅ Model evaluation metrics (MSE, MAE, RMSE, R²)
- ✅ Different network architectures
- ✅ Early stopping behavior
- ✅ Reproducibility
- ✅ Benchmark training speed

### Data Handler Module (`fivedreg.data_hand.module`)
- ✅ Loading valid datasets
- ✅ Data split ratios (60/20/20)
- ✅ Data standardization
- ✅ Input validation (shapes, keys)
- ✅ NaN value removal
- ✅ Scaler functionality
- ✅ Reproducibility

### API Endpoints (`main.py`)
- ✅ Health check endpoints (`/`, `/health`, `/status`)
- ✅ Dataset upload (`/upload-fit-dataset/`)
  - Valid uploads
  - Invalid file types
  - Invalid data formats
  - File cleanup on error
- ✅ Model training (`/start-training/`)
  - Training with valid data
  - Error handling without data
  - State management
- ✅ Prediction data upload (`/upload-predict-dataset/`)
- ✅ Batch prediction (`/start-predict/`)
- ✅ Single prediction (`/predict-single/`)
- ✅ End-to-end workflow testing

## Writing New Tests

### Unit Test Template

```python
import pytest
from your_module import YourClass

@pytest.mark.unit
@pytest.mark.fast
class TestYourClass:
    """Test suite for YourClass"""

    def test_something(self, fixture_name):
        """Test description"""
        # Arrange
        obj = YourClass()

        # Act
        result = obj.method()

        # Assert
        assert result == expected_value
```

### Integration Test Template

```python
import pytest

@pytest.mark.integration
@pytest.mark.api
class TestYourEndpoint:
    """Test suite for /your-endpoint/"""

    def test_endpoint(self, test_client):
        """Test description"""
        response = test_client.get("/your-endpoint/")

        assert response.status_code == 200
        assert "expected_key" in response.json()
```

## Continuous Integration

This test suite is designed to be run in CI/CD pipelines:

```bash
# CI command
pytest --cov=. --cov-report=xml --cov-report=term -v
```

## Troubleshooting

### Import Errors

If you encounter import errors, make sure you're in the backend directory:

```bash
cd backend
pytest
```

### Global State Issues

If tests fail due to global state, use the `reset_global_state` fixture:

```python
def test_something(self, test_client, reset_global_state):
    # Test will start with clean global state
    pass
```

### File Cleanup

Temporary files are automatically cleaned up by fixtures. If you create files manually in tests, use pytest's `tmp_path` fixture:

```python
def test_with_file(self, tmp_path):
    file_path = tmp_path / "test.pkl"
    # File will be automatically cleaned up
```

## Performance

### Test Execution Time

- Fast tests (<1s): ~40 tests
- Slow tests (>1s): ~15 tests
- Total execution time: ~30-60 seconds (depending on system)

### Optimizing Test Speed

1. Run fast tests during development:
   ```bash
   pytest -m "not slow"
   ```

2. Use parallel execution:
   ```bash
   pytest -n auto
   ```

3. Run only changed tests:
   ```bash
   pytest --lf  # Last failed
   ```

## Contributing

When adding new features, ensure:

1. Write tests for new functionality
2. Maintain >80% code coverage
3. Use appropriate test markers
4. Document fixtures and utilities
5. Keep tests fast and isolated

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
