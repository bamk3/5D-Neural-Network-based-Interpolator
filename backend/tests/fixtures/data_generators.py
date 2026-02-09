"""
Utility functions for generating test data
"""

import numpy as np
import pickle
from pathlib import Path
from typing import Dict, Tuple


def generate_linear_dataset(
    n_samples: int = 1000,
    n_features: int = 5,
    noise_level: float = 0.1,
    seed: int = 42
) -> Dict[str, np.ndarray]:
    """
    Generate a synthetic dataset with a linear relationship.

    Args:
        n_samples: Number of samples to generate
        n_features: Number of features (should be 5 for this project)
        noise_level: Standard deviation of Gaussian noise
        seed: Random seed for reproducibility

    Returns:
        Dictionary with 'X' (features) and 'y' (targets)
    """
    np.random.seed(seed)

    # Generate features
    X = np.random.randn(n_samples, n_features)

    # Generate targets with linear relationship + noise
    weights = np.array([2.0, 1.5, -0.5, 1.2, 0.8])
    y = X @ weights + np.random.randn(n_samples) * noise_level

    return {'X': X, 'y': y}


def generate_nonlinear_dataset(
    n_samples: int = 1000,
    n_features: int = 5,
    noise_level: float = 0.1,
    seed: int = 42
) -> Dict[str, np.ndarray]:
    """
    Generate a synthetic dataset with a nonlinear relationship.

    Args:
        n_samples: Number of samples to generate
        n_features: Number of features
        noise_level: Standard deviation of Gaussian noise
        seed: Random seed for reproducibility

    Returns:
        Dictionary with 'X' (features) and 'y' (targets)
    """
    np.random.seed(seed)

    # Generate features
    X = np.random.randn(n_samples, n_features)

    # Generate targets with nonlinear relationship
    y = (np.sin(X[:, 0]) * 2 +
         np.cos(X[:, 1]) * 1.5 +
         X[:, 2]**2 * 0.5 +
         np.exp(X[:, 3] * 0.1) +
         np.log(np.abs(X[:, 4]) + 1) +
         np.random.randn(n_samples) * noise_level)

    return {'X': X, 'y': y}


def generate_dataset_with_outliers(
    n_samples: int = 1000,
    n_outliers: int = 50,
    n_features: int = 5,
    seed: int = 42
) -> Dict[str, np.ndarray]:
    """
    Generate a dataset with outliers.

    Args:
        n_samples: Number of normal samples
        n_outliers: Number of outlier samples
        n_features: Number of features
        seed: Random seed

    Returns:
        Dictionary with 'X' (features) and 'y' (targets)
    """
    np.random.seed(seed)

    # Generate normal data
    X_normal = np.random.randn(n_samples, n_features)
    weights = np.array([2.0, 1.5, -0.5, 1.2, 0.8])
    y_normal = X_normal @ weights + np.random.randn(n_samples) * 0.1

    # Generate outliers
    X_outliers = np.random.randn(n_outliers, n_features) * 5  # Larger variance
    y_outliers = np.random.randn(n_outliers) * 10  # Random outlier targets

    # Combine
    X = np.vstack([X_normal, X_outliers])
    y = np.concatenate([y_normal, y_outliers])

    # Shuffle
    indices = np.random.permutation(len(X))
    X = X[indices]
    y = y[indices]

    return {'X': X, 'y': y}


def generate_dataset_with_missing_values(
    n_samples: int = 1000,
    missing_fraction: float = 0.1,
    n_features: int = 5,
    seed: int = 42
) -> Dict[str, np.ndarray]:
    """
    Generate a dataset with missing values (NaN).

    Args:
        n_samples: Number of samples
        missing_fraction: Fraction of values to set as NaN
        n_features: Number of features
        seed: Random seed

    Returns:
        Dictionary with 'X' (features) and 'y' (targets) containing NaN values
    """
    np.random.seed(seed)

    # Generate complete data
    X = np.random.randn(n_samples, n_features)
    weights = np.array([2.0, 1.5, -0.5, 1.2, 0.8])
    y = X @ weights + np.random.randn(n_samples) * 0.1

    # Introduce missing values in X
    n_missing_X = int(n_samples * n_features * missing_fraction)
    missing_indices_X = np.random.choice(n_samples * n_features, n_missing_X, replace=False)
    X_flat = X.flatten()
    X_flat[missing_indices_X] = np.nan
    X = X_flat.reshape(n_samples, n_features)

    # Introduce missing values in y
    n_missing_y = int(n_samples * missing_fraction)
    missing_indices_y = np.random.choice(n_samples, n_missing_y, replace=False)
    y[missing_indices_y] = np.nan

    return {'X': X, 'y': y}


def save_dataset(data: Dict[str, np.ndarray], filepath: str) -> None:
    """
    Save dataset to a pickle file.

    Args:
        data: Dictionary with 'X' and 'y'
        filepath: Path to save the file
    """
    with open(filepath, 'wb') as f:
        pickle.dump(data, f)


def generate_prediction_data(
    n_samples: int = 10,
    n_features: int = 5,
    seed: int = 42
) -> np.ndarray:
    """
    Generate prediction data (features only, no targets).

    Args:
        n_samples: Number of samples
        n_features: Number of features
        seed: Random seed

    Returns:
        Feature array of shape (n_samples, n_features)
    """
    np.random.seed(seed)
    return np.random.randn(n_samples, n_features)


def generate_invalid_dataset() -> Dict:
    """
    Generate various types of invalid datasets for testing error handling.

    Returns:
        Dictionary with different types of invalid data
    """
    return {
        'wrong_X_shape': {'X': np.random.randn(10, 3), 'y': np.random.randn(10)},  # X has 3 features instead of 5
        'wrong_y_shape': {'X': np.random.randn(10, 5), 'y': np.random.randn(10, 2)},  # y is 2D instead of 1D
        'mismatched_samples': {'X': np.random.randn(10, 5), 'y': np.random.randn(15)},  # Different number of samples
        'missing_X': {'y': np.random.randn(10)},  # Missing X key
        'missing_y': {'X': np.random.randn(10, 5)},  # Missing y key
        'not_dict': np.random.randn(10, 5),  # Not a dictionary
        'empty_arrays': {'X': np.array([]).reshape(0, 5), 'y': np.array([])},  # Empty arrays
    }


if __name__ == "__main__":
    # Example usage: generate test datasets
    output_dir = Path(__file__).parent / "test_data"
    output_dir.mkdir(exist_ok=True)

    # Generate and save various test datasets
    datasets = {
        'linear_small.pkl': generate_linear_dataset(n_samples=100),
        'linear_medium.pkl': generate_linear_dataset(n_samples=1000),
        'linear_large.pkl': generate_linear_dataset(n_samples=5000),
        'nonlinear.pkl': generate_nonlinear_dataset(n_samples=1000),
        'with_outliers.pkl': generate_dataset_with_outliers(),
        'with_missing.pkl': generate_dataset_with_missing_values(),
    }

    for filename, data in datasets.items():
        save_dataset(data, output_dir / filename)

    # Generate prediction data
    pred_data = generate_prediction_data(n_samples=20)
    with open(output_dir / 'prediction_data.pkl', 'wb') as f:
        pickle.dump(pred_data, f)

    print(f"Generated {len(datasets)} test datasets in {output_dir}")
