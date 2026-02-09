"""
Pytest configuration and shared fixtures for the test suite
"""

import pytest
import numpy as np
import pickle
import tempfile
import os
from pathlib import Path
from fastapi.testclient import TestClient
import sys

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def sample_data_small():
    """Generate small sample 5D dataset for quick tests"""
    np.random.seed(42)
    n_samples = 100

    # Generate 5D features
    X = np.random.randn(n_samples, 5)

    # Generate targets with a simple linear relationship
    y = (X[:, 0] * 2 + X[:, 1] * 1.5 - X[:, 2] * 0.5 +
         X[:, 3] * 1.2 + X[:, 4] * 0.8 + np.random.randn(n_samples) * 0.1)

    return {'X': X, 'y': y}


@pytest.fixture
def sample_data_medium():
    """Generate medium-sized sample 5D dataset"""
    np.random.seed(42)
    n_samples = 1000

    X = np.random.randn(n_samples, 5)
    y = (X[:, 0] * 2 + X[:, 1] * 1.5 - X[:, 2] * 0.5 +
         X[:, 3] * 1.2 + X[:, 4] * 0.8 + np.random.randn(n_samples) * 0.1)

    return {'X': X, 'y': y}


@pytest.fixture
def sample_data_large():
    """Generate large sample 5D dataset"""
    np.random.seed(42)
    n_samples = 5000

    X = np.random.randn(n_samples, 5)
    y = (X[:, 0] * 2 + X[:, 1] * 1.5 - X[:, 2] * 0.5 +
         X[:, 3] * 1.2 + X[:, 4] * 0.8 + np.random.randn(n_samples) * 0.1)

    return {'X': X, 'y': y}


@pytest.fixture
def sample_data_with_nans():
    """Generate sample data with NaN values for testing data cleaning"""
    np.random.seed(42)
    n_samples = 100

    X = np.random.randn(n_samples, 5)
    y = np.random.randn(n_samples)

    # Introduce some NaN values
    X[10:15, 2] = np.nan
    y[20:25] = np.nan

    return {'X': X, 'y': y}


@pytest.fixture
def temp_dataset_file(sample_data_small):
    """Create a temporary .pkl file with valid dataset"""
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.pkl', delete=False) as f:
        pickle.dump(sample_data_small, f)
        temp_path = f.name

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)


@pytest.fixture
def temp_dataset_file_medium(sample_data_medium):
    """Create a temporary .pkl file with medium dataset"""
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.pkl', delete=False) as f:
        pickle.dump(sample_data_medium, f)
        temp_path = f.name

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)


@pytest.fixture
def temp_predict_data():
    """Create temporary prediction data (just X features, no y)"""
    np.random.seed(42)
    X_pred = np.random.randn(10, 5)

    with tempfile.NamedTemporaryFile(mode='wb', suffix='.pkl', delete=False) as f:
        pickle.dump(X_pred, f)
        temp_path = f.name

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)


@pytest.fixture
def invalid_dataset_file():
    """Create a temporary .pkl file with invalid dataset"""
    invalid_data = {'X': np.random.randn(10, 3), 'y': np.random.randn(10)}  # Wrong X shape

    with tempfile.NamedTemporaryFile(mode='wb', suffix='.pkl', delete=False) as f:
        pickle.dump(invalid_data, f)
        temp_path = f.name

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)


@pytest.fixture
def test_client():
    """Create a FastAPI test client"""
    from main import app
    return TestClient(app)


@pytest.fixture
def uploaded_datasets_dir():
    """Ensure uploaded_datasets directory exists and clean it up after tests"""
    upload_dir = "uploaded_datasets"
    os.makedirs(upload_dir, exist_ok=True)

    yield upload_dir

    # Cleanup - remove all test files
    if os.path.exists(upload_dir):
        for file in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error removing {file_path}: {e}")


@pytest.fixture
def reset_global_state():
    """Reset global state variables before/after tests"""
    # Import main to access globals
    import main

    # Store original values
    original_values = {}
    if hasattr(main, 'processing_result'):
        original_values['processing_result'] = main.processing_result
    if hasattr(main, 'train_result'):
        original_values['train_result'] = main.train_result
    if hasattr(main, 'predict_input'):
        original_values['predict_input'] = main.predict_input

    # Reset to None
    main.processing_result = None
    main.train_result = None
    main.predict_input = None

    yield

    # Restore or keep reset
    # For tests, we'll keep them reset
    main.processing_result = None
    main.train_result = None
    main.predict_input = None


@pytest.fixture(scope="session")
def test_data_dir():
    """Create and return path to test data directory"""
    test_dir = Path(__file__).parent / "fixtures" / "test_data"
    test_dir.mkdir(parents=True, exist_ok=True)
    return test_dir


@pytest.fixture
def mock_trained_model():
    """Create a mock trained model for testing predictions"""
    from fivedreg.base_fivedreg import FastNeuralNetwork
    import numpy as np

    # Create a simple model
    model = FastNeuralNetwork(
        hidden_layers=(8, 4),
        learning_rate=0.01,
        max_iterations=10,
        early_stopping=False,
        verbose=False
    )

    # Train on dummy data
    X_dummy = np.random.randn(50, 5)
    y_dummy = np.random.randn(50)
    model.fit(X_dummy, y_dummy)

    return model
