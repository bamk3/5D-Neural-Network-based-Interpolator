Dataset Specifications
======================

Complete specification for dataset formats used by the 5D Interpolator.

Training Dataset Format
-----------------------

Structure
~~~~~~~~~

Training datasets must be Python pickle files containing a dictionary:

.. code-block:: python

   {
       'X': numpy.ndarray,  # Feature matrix
       'y': numpy.ndarray   # Target vector
   }

Requirements
~~~~~~~~~~~

**File Format:**

* Extension: ``.pkl``
* Type: Python pickle file
* Encoding: Binary

**X (Features):**

* Type: ``numpy.ndarray``
* Shape: ``(n_samples, 5)``
* Dtype: ``float32`` or ``float64``
* Values: Any real numbers (will be standardized)
* Constraints:

  * Must have exactly 5 features
  * No NaN or inf values
  * At least 100 samples recommended

**y (Targets):**

* Type: ``numpy.ndarray``
* Shape: ``(n_samples,)`` - 1D array
* Dtype: ``float32`` or ``float64``
* Values: Any real numbers
* Constraints:

  * Must match number of samples in X
  * No NaN or inf values

Example Creation
~~~~~~~~~~~~~~~

.. code-block:: python

   import numpy as np
   import pickle

   # Generate features (1000 samples, 5 features)
   X = np.random.randn(1000, 5)

   # Generate targets
   y = np.sum(X**2, axis=1)

   # Create dataset dictionary
   dataset = {'X': X, 'y': y}

   # Save as pickle
   with open('training_data.pkl', 'wb') as f:
       pickle.dump(dataset, f)

Validation
~~~~~~~~~

The system automatically validates:

✓ File is readable pickle
✓ Contains 'X' and 'y' keys
✓ X has shape (n, 5)
✓ y has shape (n,)
✓ X and y have same number of samples
✓ No NaN or inf values

Prediction Dataset Format
--------------------------

Structure
~~~~~~~~~

Prediction datasets must be Python pickle files containing a NumPy array:

.. code-block:: python

   numpy.ndarray  # Shape: (n_samples, 5)

Requirements
~~~~~~~~~~~

**File Format:**

* Extension: ``.pkl``
* Type: Python pickle file
* Encoding: Binary

**Data:**

* Type: ``numpy.ndarray``
* Shape: ``(n_samples, 5)``
* Dtype: ``float32`` or ``float64``
* Values: Any real numbers
* Constraints:

  * Must have exactly 5 features
  * No NaN or inf values
  * Any number of samples

Example Creation
~~~~~~~~~~~~~~~

.. code-block:: python

   import numpy as np
   import pickle

   # Generate prediction inputs (100 samples, 5 features)
   X_pred = np.random.randn(100, 5)

   # Save as pickle
   with open('prediction_data.pkl', 'wb') as f:
       pickle.dump(X_pred, f)

Data Preprocessing
------------------

Automatic Standardization
~~~~~~~~~~~~~~~~~~~~~~~~~

The system automatically standardizes all features using:

.. code-block:: python

   from sklearn.preprocessing import StandardScaler

   scaler = StandardScaler()
   X_scaled = scaler.fit_transform(X)

This means:

* Each feature is centered (mean = 0)
* Each feature is scaled (std = 1)
* Same transformation applied to predictions
* No manual normalization needed

Data Splitting
~~~~~~~~~~~~~

Training data is automatically split:

* **60%** Training set
* **20%** Validation set
* **20%** Test set

Split is random with fixed seed (42) for reproducibility.

Best Practices
--------------

Dataset Size
~~~~~~~~~~~

**Recommended Sizes:**

* Minimum: 100 samples
* Optimal: 1,000-10,000 samples
* Maximum: No hard limit (training time increases)

**Training Time by Size:**

* 100 samples: ~5 seconds
* 1,000 samples: ~15 seconds
* 10,000 samples: ~45 seconds
* 100,000 samples: ~5 minutes

Data Quality
~~~~~~~~~~~

**Check for:**

* Missing values (NaN)
* Infinite values (inf)
* Outliers (>3 std from mean)
* Data type consistency
* Correct dimensions

**Example Validation:**

.. code-block:: python

   import numpy as np

   def validate_dataset(X, y):
       """Validate dataset before saving"""

       # Check shapes
       assert X.ndim == 2, "X must be 2D"
       assert X.shape[1] == 5, "X must have 5 features"
       assert y.ndim == 1, "y must be 1D"
       assert X.shape[0] == y.shape[0], "X and y must have same samples"

       # Check for invalid values
       assert not np.any(np.isnan(X)), "X contains NaN"
       assert not np.any(np.isinf(X)), "X contains inf"
       assert not np.any(np.isnan(y)), "y contains NaN"
       assert not np.any(np.isinf(y)), "y contains inf"

       print(f"✓ Dataset valid: {X.shape[0]} samples, 5 features")

   # Use it
   validate_dataset(X, y)

Feature Engineering
~~~~~~~~~~~~~~~~~~

Consider:

* Feature scaling (optional, auto-standardized)
* Polynomial features for non-linear relationships
* Interaction terms
* Domain-specific transformations

Common Use Cases
----------------

Regression Problems
~~~~~~~~~~~~~~~~~~

**Example: Function Approximation**

.. code-block:: python

   # Approximate function: f(x1,...,x5) = x1^2 + x2*x3 - x4 + sin(x5)
   import numpy as np

   n = 1000
   X = np.random.randn(n, 5)
   y = X[:, 0]**2 + X[:, 1]*X[:, 2] - X[:, 3] + np.sin(X[:, 4])

Scientific Data
~~~~~~~~~~~~~~

**Example: Experimental Data**

.. code-block:: python

   # Features: temperature, pressure, concentration, time, catalyst
   # Target: reaction yield

   data = {
       'X': np.array([
           [300, 1.5, 0.1, 60, 1],  # Sample 1
           [350, 2.0, 0.2, 90, 2],  # Sample 2
           # ... more samples
       ]),
       'y': np.array([0.75, 0.82, ...])  # Yields
   }

Troubleshooting
--------------

Common Errors
~~~~~~~~~~~~

**"Invalid format: X must have shape (n, 5)"**

.. code-block:: python

   # Wrong: X is (n, 3)
   X = np.random.randn(100, 3)  # ✗

   # Correct: X is (n, 5)
   X = np.random.randn(100, 5)  # ✓

**"Invalid format: Dictionary must contain 'X' and 'y' keys"**

.. code-block:: python

   # Wrong: Missing 'y' key
   data = {'features': X}  # ✗

   # Correct: Both keys present
   data = {'X': X, 'y': y}  # ✓

**"Invalid format: X and y must have same number of samples"**

.. code-block:: python

   # Wrong: Mismatched sizes
   X = np.random.randn(100, 5)
   y = np.random.randn(90)  # ✗

   # Correct: Same size
   X = np.random.randn(100, 5)
   y = np.random.randn(100)  # ✓

Dataset Templates
-----------------

Simple Template
~~~~~~~~~~~~~~

.. code-block:: python

   """
   Simple dataset template
   """
   import numpy as np
   import pickle

   # Parameters
   n_samples = 1000

   # Generate data
   X = np.random.randn(n_samples, 5)
   y = np.sum(X, axis=1)  # Simple sum

   # Save
   with open('simple_dataset.pkl', 'wb') as f:
       pickle.dump({'X': X, 'y': y}, f)

Complex Template
~~~~~~~~~~~~~~~

.. code-block:: python

   """
   Complex dataset template with validation
   """
   import numpy as np
   import pickle

   def create_dataset(n_samples, noise_level=0.1, seed=42):
       """Create validated dataset"""
       np.random.seed(seed)

       # Generate features
       X = np.random.randn(n_samples, 5)

       # Complex target function
       y = (X[:, 0]**2 +
            X[:, 1]*X[:, 2] -
            np.sin(X[:, 3]) +
            np.log1p(np.abs(X[:, 4])))

       # Add noise
       y += noise_level * np.random.randn(n_samples)

       # Validate
       assert X.shape == (n_samples, 5)
       assert y.shape == (n_samples,)
       assert not np.any(np.isnan(X))
       assert not np.any(np.isnan(y))

       return {'X': X, 'y': y}

   # Create and save
   dataset = create_dataset(1000)
   with open('complex_dataset.pkl', 'wb') as f:
       pickle.dump(dataset, f)

Next Steps
----------

* :doc:`quickstart` - Upload and use datasets
* :doc:`usage` - Detailed usage guide
* :doc:`api/backend` - API for dataset upload
