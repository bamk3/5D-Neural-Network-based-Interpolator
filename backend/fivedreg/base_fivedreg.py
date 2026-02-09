"""
Fast Neural Network for 5D Interpolation
Optimized for CPU training in under 1 minute on datasets up to 10,000 samples

Key features:
- Small, efficient default architecture (default: [64, 32, 16]) but as instructed in the coursework, a user can change them using provided sliders)
- Fully configurable (layers, neurons, learning rate, iterations)
- Optimized for fast CPU training (under 1 minute on datasets up to 10,000 samples)
- Early stopping to prevent wasted computation
"""


import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import time

from .data_hand.module import load_dataset



class FastNeuralNetwork:
    """
    Fast, fully configurable neural network for 5D interpolation.

    Optimized for CPU training in under 1 minute on datasets up to 10,000 samples.

    Parameters:
    -----------
    hidden_layers : tuple or list
        Number of neurons in each hidden layer (default: (64, 32, 16))
    learning_rate : float
        Learning rate for Adam optimizer (default: 0.001)
    max_iterations : int
        Maximum number of training iterations (default: 500)
    early_stopping : bool
        Use early stopping to save time (default: True)
    verbose : bool
        Print training progress (default: True)

    Example:
    --------
    >>> model = FastNeuralNetwork(
    ...     hidden_layers=(64, 32, 16),  # Default, but as instructed in the coursework, a user can change them using provided sliders)
    ...     learning_rate=0.001,
    ...     max_iterations=500)
    >>> model.fit(X_train, y_train)
    >>> predictions = model.predict(X_test)
    """

    def __init__(
        self,
        hidden_layers=(64, 32, 16),
        learning_rate=0.001,
        max_iterations=500,
        early_stopping=True,
        verbose=False):
        """
        Initialize the fast neural network.

        Args:
            hidden_layers: Tuple of neurons per layer (e.g., (64, 32, 16))
            learning_rate: Learning rate for optimization (default: 0.001)
            max_iterations: Maximum training iterations (default: 500)
            early_stopping: Enable early stopping (default: True)
            verbose: Print training progress (default: True)
        """
        self.hidden_layers = tuple(hidden_layers)
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.early_stopping = early_stopping
        self.verbose = verbose

        # Build the model
        self.model = MLPRegressor(
            hidden_layer_sizes=self.hidden_layers,
            activation='relu',
            solver='adam',
            alpha=0.0001,  # L2 regularization
            batch_size='auto',  # Auto-select optimal batch size
            learning_rate='adaptive',  # Adaptive learning rate for speed
            learning_rate_init=self.learning_rate,
            max_iter=self.max_iterations,
            shuffle=True,
            random_state=42,
            early_stopping=self.early_stopping,
            validation_fraction=0.1 if self.early_stopping else 0,
            n_iter_no_change=20,  # Faster early stopping
            tol=1e-4,  # Tolerance for optimization
            verbose=self.verbose)

        self.training_time_ = None
        self.n_iterations_ = None

    def fit(self, X_train, y_train):
        """
        Train the neural network.

        Args:
            X_train: Training features (n_samples, 5)
            y_train: Training targets (n_samples,)

        Returns:
            self
        """
        if self.verbose:
            print("\n" + "="*60)
            print("FAST NEURAL NETWORK - Training")
            print("="*60)
            print(f"Architecture: {self.hidden_layers}")
            print(f"Learning rate: {self.learning_rate}")
            print(f"Max iterations: {self.max_iterations}")
            print(f"Early stopping: {self.early_stopping}")
            print(f"Training samples: {len(X_train)}")
            print("="*60 + "\n")

        start_time = time.time()

        # Train the model
        self.model.fit(X_train, y_train)

        self.training_time_ = time.time() - start_time
        self.n_iterations_ = self.model.n_iter_

        if self.verbose:
            print("\n" + "="*60)
            print(f"Training completed in {self.training_time_:.2f} seconds")
            print(f"Iterations: {self.n_iterations_}")
            print(f"Final loss: {self.model.loss_:.6f}")
            print("="*60)

        return self

    def predict(self, X):
        """
        Make predictions.

        Args:
            X: Features to predict (n_samples, 5)

        Returns:
            Predictions (n_samples,)
        """
        return self.model.predict(X)

    def evaluate(self, X, y, dataset_name="Test"):
        """
        Evaluate the model with regression metrics.

        Args:
            X: Features
            y: True targets
            dataset_name: Name for printing (default: "Test")

        Returns:
            Dictionary with MAE, MSE, RMSE, and R² score
        """
        y_pred = self.predict(X)

        # Calculate metrics
        mse = mean_squared_error(y, y_pred)
        mae = mean_absolute_error(y, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y, y_pred)

        metrics = {
            'mse': mse,
            'mae': mae,
            'rmse': rmse,
            'r2': r2
        }

        if self.verbose:
            print(f"\n{dataset_name} Set Evaluation:")
            print(f"  MAE:  {mae:.6f}")
            print(f"  RMSE: {rmse:.6f}")
            print(f"  R²:   {r2:.6f}")

        return metrics

    def get_params(self):
        """Get model configuration."""
        return {
            'hidden_layers': self.hidden_layers,
            'learning_rate': self.learning_rate,
            'max_iterations': self.max_iterations,
            'early_stopping': self.early_stopping,
            'training_time': self.training_time_,
            'iterations': self.n_iterations_
        }


def benchmark_training_speed(dataset_path, hidden_layers=(64, 32, 16), learning_rate=0.001,
                            max_iterations=500, early_stopping=True):
    """
    Benchmark training speed on the dataset with configurable hyperparameters.

    Args:
        dataset_path: Path to the dataset file
        hidden_layers: Tuple of neurons per layer (default: (64, 32, 16)) fully configure as instructed in the coursework by the professeur.
        learning_rate: Learning rate for optimization (default: 0.001)
        max_iterations: Maximum training iterations (default: 500)
        early_stopping: Enable early stopping (default: True)
    """
   # print("\n" + "="*60)
    #print("FAST NEURAL NETWORK - SPEED BENCHMARK")
    #print("="*60)

    # Load dataset
    X_train, y_train, X_val, y_val, X_test, y_test, scaler_X, scaler_y = load_dataset(dataset_path)

    # Combine train and val
    X_train_full = np.vstack([X_train, X_val])
    y_train_full = np.concatenate([y_train, y_val])

    # Create model with configurable architecture
    global model
    model = FastNeuralNetwork(
        hidden_layers=hidden_layers,
        learning_rate=learning_rate,
        max_iterations=max_iterations,
        early_stopping=early_stopping,
        verbose=False # Suppress output for benchmark
    )

    # Train
    model.fit(X_train_full, y_train_full)

    # Evaluate
    metrics = model.evaluate(X_test, y_test, "Test")

    print("\n" + "="*60)
    print(f"Architecture: {hidden_layers}")
    print(f"Learning rate: {learning_rate}")
    print(f"Max iterations: {max_iterations}")
    print(f"Early stopping: {early_stopping}")
    #if params['training_time'] < 60:
       # print(f"✓ PASSED: Training time ({params['training_time']:.2f}s) < 60s")
    #else:
     #   print(f"✗ FAILED: Training time ({params['training_time']:.2f}s) >= 60s")

    if metrics['r2'] > 0.95:
        print(f"✓ PASSED: R² score ({metrics['r2']:.4f}) > 0.95")
    else:
        print(f"⚠ WARNING: R² score ({metrics['r2']:.4f}) < 0.95")

    print("="*60)

    return model, metrics

def start_predict(dataset_path):
    """
    Make predictions using the trained model.
    """
    return model.predict(dataset_path)


def demonstrate_configurability(dataset_path):
    """
    Demonstrate full configurability of the model.
    """
    print("\n" + "="*60)
    print("DEMONSTRATING CONFIGURABILITY")
    print("="*60)

    # Load dataset
    X_train, y_train, X_val, y_val, X_test, y_test, scaler_X, scaler_y = load_dataset(dataset_path)
    X_train_full = np.vstack([X_train, X_val])
    y_train_full = np.concatenate([y_train, y_val])

    configurations = [
        {
            'name': 'Default (3 layers)',
            'hidden_layers': (64, 32, 16),
            'learning_rate': 0.001,
            'max_iterations': 500
        },
        {
            'name': 'Shallow (2 layers)',
            'hidden_layers': (128, 64),
            'learning_rate': 0.001,
            'max_iterations': 500
        },
        {
            'name': 'Deep (4 layers)',
            'hidden_layers': (64, 64, 32, 16),
            'learning_rate': 0.001,
            'max_iterations': 500
        },
        {
            'name': 'Fast (low iterations)',
            'hidden_layers': (64, 32, 16),
            'learning_rate': 0.01,  # Higher learning rate
            'max_iterations': 200
        }
    ]

    results = []

    for config in configurations:
        print(f"\n{'='*60}")
        print(f"Configuration: {config['name']}")
        print(f"{'='*60}")

        model = FastNeuralNetwork(
            hidden_layers=config['hidden_layers'],
            learning_rate=config['learning_rate'],
            max_iterations=config['max_iterations'],
            early_stopping=True,
            verbose=False  
        )

        start = time.time()
        model.fit(X_train_full, y_train_full)
        train_time = time.time() - start

        metrics = model.evaluate(X_test, y_test, config['name'])

        results.append({
            'name': config['name'],
            'architecture': config['hidden_layers'],
            'lr': config['learning_rate'],
            'max_iter': config['max_iterations'],
            'time': train_time,
            'iterations': model.n_iterations_,
            'r2': metrics['r2'],
            'mae': metrics['mae']})

   


