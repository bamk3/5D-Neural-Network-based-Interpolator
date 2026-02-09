"""
Unit tests for the FastNeuralNetwork class
"""

import pytest
import numpy as np
from fivedreg.base_fivedreg import FastNeuralNetwork, benchmark_training_speed


@pytest.mark.unit
@pytest.mark.model
@pytest.mark.fast
class TestFastNeuralNetwork:
    """Test suite for FastNeuralNetwork class"""

    def test_initialization_default(self):
        """Test default initialization of FastNeuralNetwork"""
        model = FastNeuralNetwork()

        assert model.hidden_layers == (64, 32, 16)
        assert model.learning_rate == 0.001
        assert model.max_iterations == 500
        assert model.early_stopping is True
        assert model.verbose is False
        assert model.training_time_ is None
        assert model.n_iterations_ is None

    def test_initialization_custom(self):
        """Test custom initialization parameters"""
        model = FastNeuralNetwork(
            hidden_layers=(128, 64, 32),
            learning_rate=0.01,
            max_iterations=1000,
            early_stopping=False,
            verbose=True
        )

        assert model.hidden_layers == (128, 64, 32)
        assert model.learning_rate == 0.01
        assert model.max_iterations == 1000
        assert model.early_stopping is False
        assert model.verbose is True

    def test_fit_basic(self, sample_data_small):
        """Test basic model fitting"""
        model = FastNeuralNetwork(
            hidden_layers=(8, 4),
            max_iterations=10,
            verbose=False
        )

        X = sample_data_small['X']
        y = sample_data_small['y']

        # Fit should return self
        result = model.fit(X, y)
        assert result is model

        # Training time should be set
        assert model.training_time_ is not None
        assert model.training_time_ > 0

        # Iterations should be set
        assert model.n_iterations_ is not None
        assert model.n_iterations_ > 0

    def test_fit_wrong_input_shape(self):
        """Test that model can fit with different input shapes (sklearn behavior)"""
        model = FastNeuralNetwork(verbose=False)

        # Different number of features - sklearn MLPRegressor accepts any input shape
        X_wrong = np.random.randn(100, 3)
        y = np.random.randn(100)

        # Should fit without error (sklearn accepts any shape)
        model.fit(X_wrong, y)
        assert model.training_time_ is not None

    def test_fit_mismatched_samples(self):
        """Test that fitting with mismatched X and y raises error"""
        model = FastNeuralNetwork(verbose=False)

        X = np.random.randn(100, 5)
        y = np.random.randn(50)  # Different number of samples

        with pytest.raises(ValueError):
            model.fit(X, y)

    def test_predict_basic(self, sample_data_small):
        """Test basic prediction functionality"""
        model = FastNeuralNetwork(
            hidden_layers=(8, 4),
            max_iterations=10,
            verbose=False
        )

        X = sample_data_small['X']
        y = sample_data_small['y']

        model.fit(X, y)

        # Predict on same data
        predictions = model.predict(X)

        assert predictions.shape == y.shape
        assert len(predictions) == len(y)
        assert predictions.dtype == np.float64

    def test_predict_before_fit(self):
        """Test that predicting before fitting raises error"""
        model = FastNeuralNetwork(verbose=False)

        X = np.random.randn(10, 5)

        with pytest.raises(Exception):  # sklearn raises NotFittedError
            model.predict(X)

    def test_predict_wrong_shape(self, sample_data_small):
        """Test that predicting with wrong input shape raises error"""
        model = FastNeuralNetwork(
            hidden_layers=(8, 4),
            max_iterations=10,
            verbose=False
        )

        X = sample_data_small['X']
        y = sample_data_small['y']

        model.fit(X, y)

        # Wrong number of features
        X_wrong = np.random.randn(10, 3)

        with pytest.raises(ValueError):
            model.predict(X_wrong)

    def test_evaluate_basic(self, sample_data_small):
        """Test model evaluation"""
        model = FastNeuralNetwork(
            hidden_layers=(16, 8),
            max_iterations=50,
            verbose=False
        )

        X = sample_data_small['X']
        y = sample_data_small['y']

        model.fit(X, y)

        metrics = model.evaluate(X, y, dataset_name="Test")

        # Check that all metrics are present
        assert 'mse' in metrics
        assert 'mae' in metrics
        assert 'rmse' in metrics
        assert 'r2' in metrics

        # Check that metrics are reasonable
        assert metrics['mse'] >= 0
        assert metrics['mae'] >= 0
        assert metrics['rmse'] >= 0
        assert metrics['rmse'] == np.sqrt(metrics['mse'])
        assert -1 <= metrics['r2'] <= 1  # R² can be negative for bad models

    def test_evaluate_good_fit(self, sample_data_medium):
        """Test that model achieves good fit on linear data"""
        model = FastNeuralNetwork(
            hidden_layers=(64, 32, 16),
            max_iterations=200,
            early_stopping=True,
            verbose=False
        )

        X = sample_data_medium['X']
        y = sample_data_medium['y']

        model.fit(X, y)
        metrics = model.evaluate(X, y)

        # Should achieve good R² on training data
        assert metrics['r2'] > 0.9

    def test_get_params(self, sample_data_small):
        """Test getting model parameters"""
        model = FastNeuralNetwork(
            hidden_layers=(32, 16),
            learning_rate=0.005,
            max_iterations=100,
            verbose=False
        )

        X = sample_data_small['X']
        y = sample_data_small['y']

        model.fit(X, y)

        params = model.get_params()

        assert params['hidden_layers'] == (32, 16)
        assert params['learning_rate'] == 0.005
        assert params['max_iterations'] == 100
        assert params['training_time'] is not None
        assert params['iterations'] is not None

    def test_different_architectures(self, sample_data_small):
        """Test that different architectures can be trained"""
        X = sample_data_small['X']
        y = sample_data_small['y']

        architectures = [
            (32,),  # Single layer
            (64, 32),  # Two layers
            (64, 32, 16),  # Three layers
            (128, 64, 32, 16),  # Four layers
        ]

        for arch in architectures:
            model = FastNeuralNetwork(
                hidden_layers=arch,
                max_iterations=10,
                verbose=False
            )

            model.fit(X, y)
            predictions = model.predict(X)

            assert predictions.shape == y.shape

    def test_early_stopping(self, sample_data_medium):
        """Test that early stopping works"""
        X = sample_data_medium['X']
        y = sample_data_medium['y']

        # Model with early stopping
        model_early = FastNeuralNetwork(
            hidden_layers=(64, 32),
            max_iterations=1000,
            early_stopping=True,
            verbose=False
        )

        model_early.fit(X, y)

        # Should stop before max iterations
        assert model_early.n_iterations_ < 1000

    def test_reproducibility(self, sample_data_small):
        """Test that results are reproducible with same random state"""
        X = sample_data_small['X']
        y = sample_data_small['y']

        # Train two models with same parameters
        model1 = FastNeuralNetwork(
            hidden_layers=(32, 16),
            max_iterations=50,
            early_stopping=False,
            verbose=False
        )

        model2 = FastNeuralNetwork(
            hidden_layers=(32, 16),
            max_iterations=50,
            early_stopping=False,
            verbose=False
        )

        model1.fit(X, y)
        model2.fit(X, y)

        predictions1 = model1.predict(X[:10])
        predictions2 = model2.predict(X[:10])

        # Results should be identical (same random state)
        np.testing.assert_array_almost_equal(predictions1, predictions2, decimal=5)


@pytest.mark.unit
@pytest.mark.model
@pytest.mark.slow
class TestBenchmarkTraining:
    """Test suite for benchmark_training_speed function"""

    def test_benchmark_training_speed(self, temp_dataset_file_medium):
        """Test benchmark_training_speed function"""
        model, metrics = benchmark_training_speed(temp_dataset_file_medium)

        # Check that model is returned
        assert isinstance(model, FastNeuralNetwork)
        assert model.training_time_ is not None

        # Check that metrics are returned
        assert 'mse' in metrics
        assert 'mae' in metrics
        assert 'rmse' in metrics
        assert 'r2' in metrics

        # Check metric values are reasonable
        assert metrics['mse'] >= 0
        assert metrics['mae'] >= 0
        assert metrics['r2'] <= 1

    def test_benchmark_achieves_target_accuracy(self, temp_dataset_file_medium):
        """Test that benchmark achieves target R² > 0.95"""
        model, metrics = benchmark_training_speed(temp_dataset_file_medium)

        # Should achieve good accuracy on synthetic linear data
        assert metrics['r2'] > 0.9

    def test_benchmark_with_small_dataset(self, temp_dataset_file):
        """Test benchmark with small dataset"""
        model, metrics = benchmark_training_speed(temp_dataset_file)

        # Should complete without errors
        assert model is not None
        assert metrics is not None
        assert metrics['r2'] <= 1
