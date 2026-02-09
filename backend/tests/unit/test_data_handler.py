"""
Unit tests for data handling module
"""

import pytest
import numpy as np
import pickle
import tempfile
import os
from fivedreg.data_hand.module import load_dataset


@pytest.mark.unit
@pytest.mark.data
@pytest.mark.fast
class TestLoadDataset:
    """Test suite for load_dataset function"""

    def test_load_valid_dataset(self, temp_dataset_file):
        """Test loading a valid dataset"""
        X_train, y_train, X_val, y_val, X_test, y_test, scaler_X, scaler_y = load_dataset(
            temp_dataset_file
        )

        # Check that all outputs are not None
        assert X_train is not None
        assert y_train is not None
        assert X_val is not None
        assert y_val is not None
        assert X_test is not None
        assert y_test is not None
        assert scaler_X is not None
        assert scaler_y is not None

        # Check shapes
        assert X_train.shape[1] == 5
        assert X_val.shape[1] == 5
        assert X_test.shape[1] == 5

        assert len(y_train.shape) == 1
        assert len(y_val.shape) == 1
        assert len(y_test.shape) == 1

        # Check that number of samples match
        assert X_train.shape[0] == y_train.shape[0]
        assert X_val.shape[0] == y_val.shape[0]
        assert X_test.shape[0] == y_test.shape[0]

    def test_data_split_ratios(self, temp_dataset_file_medium):
        """Test that data is split with correct ratios (60/20/20)"""
        X_train, y_train, X_val, y_val, X_test, y_test, scaler_X, scaler_y = load_dataset(
            temp_dataset_file_medium
        )

        total_samples = len(X_train) + len(X_val) + len(X_test)

        # Check approximate split ratios (within 5% tolerance)
        train_ratio = len(X_train) / total_samples
        val_ratio = len(X_val) / total_samples
        test_ratio = len(X_test) / total_samples

        assert 0.55 < train_ratio < 0.65  # ~60%
        assert 0.15 < val_ratio < 0.25    # ~20%
        assert 0.15 < test_ratio < 0.25   # ~20%

    def test_standardization(self, temp_dataset_file):
        """Test that data is properly standardized"""
        X_train, y_train, X_val, y_val, X_test, y_test, scaler_X, scaler_y = load_dataset(
            temp_dataset_file
        )

        # Training data should have approximately mean=0, std=1
        assert np.abs(X_train.mean()) < 0.1
        assert np.abs(X_train.std() - 1.0) < 0.2

        assert np.abs(y_train.mean()) < 0.1
        assert np.abs(y_train.std() - 1.0) < 0.2

    def test_load_invalid_shape_X(self):
        """Test that loading dataset with invalid X shape raises error"""
        # Create invalid dataset (X has 3 features instead of 5)
        invalid_data = {
            'X': np.random.randn(100, 3),
            'y': np.random.randn(100)
        }

        with tempfile.NamedTemporaryFile(mode='wb', suffix='.pkl', delete=False) as f:
            pickle.dump(invalid_data, f)
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="Expected X with 5 features"):
                load_dataset(temp_path)
        finally:
            os.remove(temp_path)

    def test_load_invalid_shape_y(self):
        """Test that loading dataset with invalid y shape raises error"""
        # Create invalid dataset (y is 2D instead of 1D)
        invalid_data = {
            'X': np.random.randn(100, 5),
            'y': np.random.randn(100, 2)
        }

        with tempfile.NamedTemporaryFile(mode='wb', suffix='.pkl', delete=False) as f:
            pickle.dump(invalid_data, f)
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="1D y"):
                load_dataset(temp_path)
        finally:
            os.remove(temp_path)

    def test_load_missing_keys(self):
        """Test that loading dataset with missing keys raises error"""
        # Missing 'y' key
        invalid_data = {'X': np.random.randn(100, 5)}

        with tempfile.NamedTemporaryFile(mode='wb', suffix='.pkl', delete=False) as f:
            pickle.dump(invalid_data, f)
            temp_path = f.name

        try:
            with pytest.raises(KeyError):
                load_dataset(temp_path)
        finally:
            os.remove(temp_path)

    def test_load_dataset_with_nans(self, sample_data_with_nans):
        """Test that NaN values are properly removed"""
        # Create temp file with NaN data
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.pkl', delete=False) as f:
            pickle.dump(sample_data_with_nans, f)
            temp_path = f.name

        try:
            X_train, y_train, X_val, y_val, X_test, y_test, scaler_X, scaler_y = load_dataset(
                temp_path
            )

            # Check that no NaN values remain
            assert not np.isnan(X_train).any()
            assert not np.isnan(y_train).any()
            assert not np.isnan(X_val).any()
            assert not np.isnan(y_val).any()
            assert not np.isnan(X_test).any()
            assert not np.isnan(y_test).any()

            # Total samples should be less than original due to NaN removal
            total_samples = len(X_train) + len(X_val) + len(X_test)
            assert total_samples < 100  # Original had 100 samples with some NaN

        finally:
            os.remove(temp_path)

    def test_scaler_transformation(self, temp_dataset_file):
        """Test that scalers can transform new data"""
        X_train, y_train, X_val, y_val, X_test, y_test, scaler_X, scaler_y = load_dataset(
            temp_dataset_file
        )

        # Generate new data
        X_new = np.random.randn(10, 5)

        # Should be able to transform with scaler_X
        X_new_scaled = scaler_X.transform(X_new)

        assert X_new_scaled.shape == X_new.shape

        # Generate new targets
        y_new = np.random.randn(10)

        # Should be able to transform with scaler_y
        y_new_scaled = scaler_y.transform(y_new.reshape(-1, 1)).flatten()

        assert y_new_scaled.shape == y_new.shape

    def test_load_file_not_found(self):
        """Test that loading non-existent file raises error"""
        with pytest.raises(FileNotFoundError):
            load_dataset("/nonexistent/path/to/file.pkl")

    def test_reproducibility(self, temp_dataset_file):
        """Test that loading same file twice gives same split"""
        result1 = load_dataset(temp_dataset_file)
        result2 = load_dataset(temp_dataset_file)

        X_train1, y_train1 = result1[0], result1[1]
        X_train2, y_train2 = result2[0], result2[1]

        # Should have same data (same random state used in train_test_split)
        np.testing.assert_array_almost_equal(X_train1, X_train2)
        np.testing.assert_array_almost_equal(y_train1, y_train2)

    def test_dataset_statistics(self, temp_dataset_file_medium):
        """Test that dataset statistics are computed correctly"""
        X_train, y_train, X_val, y_val, X_test, y_test, scaler_X, scaler_y = load_dataset(
            temp_dataset_file_medium
        )

        # scaler_X should have learned mean and std for each feature
        assert scaler_X.mean_.shape == (5,)
        assert scaler_X.scale_.shape == (5,)

        # scaler_y should have learned mean and std for target
        assert scaler_y.mean_.shape == (1,)
        assert scaler_y.scale_.shape == (1,)
