Usage Guide
===========

Comprehensive guide to using the 5D Neural Network Interpolator.

Application Workflow
--------------------

The typical workflow consists of three main steps:

1. **Upload Training Dataset** → 2. **Train Model** → 3. **Make Predictions**

Step 1: Upload Training Dataset
--------------------------------

Navigate to the Upload page and select a training dataset.

Dataset Requirements
~~~~~~~~~~~~~~~~~~~

The training dataset must be a Python pickle file (``.pkl``) containing:

.. code-block:: python

   {
       'X': numpy.ndarray,  # Shape: (n_samples, 5)
       'y': numpy.ndarray   # Shape: (n_samples,)
   }

Where:

* ``X``: 5-dimensional feature vectors (independent variables)
* ``y``: 1-dimensional target values (dependent variable)
* ``n_samples``: Number of training examples

Example Dataset Creation
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import numpy as np
   import pickle

   # Generate 1000 samples
   n_samples = 1000

   # Create 5D features
   X = np.random.randn(n_samples, 5)

   # Create target (example: sum of squares)
   y = np.sum(X**2, axis=1) + 0.1 * np.random.randn(n_samples)

   # Save as pickle
   data = {'X': X, 'y': y}
   with open('training_data.pkl', 'wb') as f:
       pickle.dump(data, f)

Upload Process
~~~~~~~~~~~~~

1. Click **"Training"** dataset type
2. Click upload area or drag file
3. Wait for validation
4. Review data preview showing:

   * Total samples
   * Data shape
   * First 5 rows

5. Click **"Proceed to Training →"**

Step 2: Train Model
-------------------

Configure hyperparameters and train the neural network.

Hyperparameter Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Neural Network Architecture**

* **Hidden Layer 1** (8-256 neurons)

  * Controls first layer capacity
  * Default: 64 neurons
  * Larger = more complex patterns

* **Hidden Layer 2** (8-128 neurons)

  * Controls second layer capacity
  * Default: 32 neurons
  * Typically smaller than layer 1

* **Hidden Layer 3** (4-64 neurons)

  * Controls third layer capacity
  * Default: 16 neurons
  * Smallest layer before output

**Training Parameters**

* **Learning Rate** (0.0001-0.01)

  * Speed of gradient descent
  * Default: 0.001
  * Higher = faster but less stable
  * Lower = slower but more precise

* **Max Iterations** (100-2000)

  * Maximum training epochs
  * Default: 500
  * Higher = more training time
  * May stop early if enabled

* **Early Stopping** (On/Off)

  * Stops when validation loss plateaus
  * Default: On (recommended)
  * Prevents overfitting
  * Saves computation time

Recommended Configurations
~~~~~~~~~~~~~~~~~~~~~~~~~

**Default (Balanced)**

.. code-block:: text

   Architecture: [64, 32, 16]
   Learning Rate: 0.001
   Max Iterations: 500
   Early Stopping: On

   Use for: Most datasets
   Expected time: 15-30 seconds

**Fast Training**

.. code-block:: text

   Architecture: [32, 16, 8]
   Learning Rate: 0.01
   Max Iterations: 200
   Early Stopping: On

   Use for: Quick experiments
   Expected time: 5-10 seconds

**High Accuracy**

.. code-block:: text

   Architecture: [128, 64, 32]
   Learning Rate: 0.001
   Max Iterations: 1000
   Early Stopping: On

   Use for: Best possible fit
   Expected time: 30-60 seconds

Training Process
~~~~~~~~~~~~~~~

1. Adjust sliders to desired values
2. Click **"Start Training"**
3. Wait for training (typically <1 minute)
4. Review results

Understanding Training Results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After training completes, you'll see:

**Performance Metrics**

* **R² Score**: Model fit quality (0-1)

  * >0.95: Excellent
  * 0.90-0.95: Very good
  * 0.80-0.90: Good
  * <0.80: May need tuning

* **MSE (Mean Squared Error)**: Average squared error

  * Lower is better
  * Scale depends on target values

* **MAE (Mean Absolute Error)**: Average absolute error

  * Lower is better
  * Same units as target variable

* **RMSE (Root Mean Squared Error)**: Square root of MSE

  * Lower is better
  * Same units as target variable

**Hyperparameters Used**

Displays the configuration used for training.

Step 3: Make Predictions
-------------------------

Two prediction modes are available.

Batch Prediction
~~~~~~~~~~~~~~~

For predicting multiple samples at once.

**Dataset Requirements:**

.. code-block:: python

   # Pickle file containing only X data
   X_pred = numpy.ndarray  # Shape: (n_samples, 5)

**Example:**

.. code-block:: python

   import numpy as np
   import pickle

   # Create prediction inputs
   X_pred = np.random.randn(100, 5)

   # Save as pickle
   with open('prediction_data.pkl', 'wb') as f:
       pickle.dump(X_pred, f)

**Steps:**

1. Upload prediction dataset (Upload page)
2. Go to Predict page
3. Select **"Batch Prediction"**
4. Click **"Generate Batch Predictions"**
5. View results

Single Prediction
~~~~~~~~~~~~~~~~

For predicting one sample at a time.

**Steps:**

1. Go to Predict page
2. Select **"Single Prediction"**
3. Enter values for all 5 features
4. Click **"Predict"**
5. View result

**Example Input:**

.. code-block:: text

   Feature 1: 1.2345
   Feature 2: -0.5678
   Feature 3: 0.9876
   Feature 4: -1.2345
   Feature 5: 0.5432

   Result: 3.456789

Advanced Usage
--------------

Experimenting with Hyperparameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To compare different configurations:

1. Train with configuration A
2. Note R² score
3. Go to Upload page
4. Re-upload SAME dataset (resets state)
5. Return to Train page
6. Train with configuration B
7. Compare results

API Usage
~~~~~~~~~

For programmatic access, use the REST API:

.. code-block:: python

   import requests

   BASE_URL = "http://localhost:8000"

   # Upload dataset
   with open('data.pkl', 'rb') as f:
       r = requests.post(
           f"{BASE_URL}/upload-fit-dataset/",
           files={'file': f}
       )

   # Train with custom hyperparameters
   r = requests.post(
       f"{BASE_URL}/start-training/",
       json={
           "hyperparameters": {
               "hidden_layer_1": 128,
               "learning_rate": 0.01
           }
       }
   )

   # Make prediction
   r = requests.post(
       f"{BASE_URL}/predict-single/",
       json={"features": [1, 2, 3, 4, 5]}
   )

   print(r.json())

See :doc:`api/backend` for complete API reference.

Tips and Best Practices
------------------------

Dataset Preparation
~~~~~~~~~~~~~~~~~~

* Remove NaN/inf values before upload
* Ensure consistent data types
* Check for outliers
* Recommended size: 1,000-10,000 samples

Model Training
~~~~~~~~~~~~~

* Start with defaults
* Increase complexity if R² < 0.9
* Reduce complexity if overfitting
* Use early stopping for efficiency
* Monitor training time

Prediction
~~~~~~~~~~

* Ensure prediction data matches training scale
* Use batch mode for efficiency
* Single mode good for testing
* Validate results against known values

Troubleshooting
--------------

Training Issues
~~~~~~~~~~~~~~

**R² score too low (<0.8):**

* Increase network size
* Increase iterations
* Try different learning rate
* Check data quality

**Training too slow (>60 seconds):**

* Reduce network size
* Reduce iterations
* Enable early stopping
* Use smaller dataset

**Model fails to converge:**

* Reduce learning rate
* Increase iterations
* Check for data issues

Prediction Issues
~~~~~~~~~~~~~~~~

**Predictions seem wrong:**

* Verify model is trained
* Check prediction data format
* Ensure feature scales match training
* Review R² score

**Batch prediction fails:**

* Verify data shape (n, 5)
* Check file format (.pkl)
* Ensure model is trained

Keyboard Shortcuts
------------------

While using the application:

* **Refresh page**: Reset state
* **Browser back**: Navigate between pages
* **Ctrl/Cmd + Click link**: Open in new tab

Next Steps
----------

* :doc:`api/backend` - API reference
* :doc:`testing/overview` - Run tests
* :doc:`datasets` - Dataset specifications
