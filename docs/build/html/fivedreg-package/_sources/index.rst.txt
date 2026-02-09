fivedreg Package Documentation
==============================

Welcome to the **fivedreg** package documentation. This package provides a fast, CPU-optimized neural network for 5D function interpolation.

.. image:: https://img.shields.io/badge/python-3.9+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python Version

.. image:: https://img.shields.io/badge/version-0.1.0-brightgreen.svg
   :alt: Version

Overview
--------

**fivedreg** is a lightweight neural network package designed for fast 5D interpolation on CPU. It features:

* **Fast Training**: Optimized for CPU training in under 1 minute on datasets up to 10,000 samples
* **Configurable Architecture**: Fully customizable hidden layers, learning rate, and iterations
* **Automatic Preprocessing**: Built-in data validation, NaN removal, and standardization
* **Early Stopping**: Prevents overfitting and saves computation time
* **scikit-learn Backend**: Built on MLPRegressor for reliability and performance

Quick Example
-------------

.. code-block:: python

   from fivedreg import benchmark_training_speed

   # Train a model on your dataset
   model, metrics = benchmark_training_speed(
       dataset_path='data.pkl',
       hidden_layers=(128, 64, 32),
       learning_rate=0.001,
       max_iterations=500
   )

   # Make predictions
   predictions = model.predict(X_new)

   # Check performance
   print(f"R² Score: {metrics['r2']:.4f}")

Installation
------------

The package is installed automatically when you set up the backend:

.. code-block:: bash

   cd backend
   pip install -e .

Or install dependencies directly:

.. code-block:: bash

   pip install numpy pandas scikit-learn

Package Contents
----------------

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   modules/core
   modules/data_handling

Module Reference
----------------

Core Neural Network Module
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: fivedreg.base_fivedreg
   :no-members:
   :no-undoc-members:

FastNeuralNetwork Class
^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: fivedreg.base_fivedreg.FastNeuralNetwork
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

   .. rubric:: Methods

   .. autosummary::
      :nosignatures:

      ~FastNeuralNetwork.__init__
      ~FastNeuralNetwork.fit
      ~FastNeuralNetwork.predict
      ~FastNeuralNetwork.evaluate
      ~FastNeuralNetwork.get_params

Top-Level Functions
^^^^^^^^^^^^^^^^^^^

.. autofunction:: fivedreg.base_fivedreg.benchmark_training_speed

.. autofunction:: fivedreg.base_fivedreg.start_predict

.. autofunction:: fivedreg.base_fivedreg.demonstrate_configurability

Data Handling Module
~~~~~~~~~~~~~~~~~~~~

.. automodule:: fivedreg.data_hand.module
   :no-members:
   :no-undoc-members:

.. autofunction:: fivedreg.data_hand.module.load_dataset

Usage Examples
--------------

Basic Training
~~~~~~~~~~~~~~

.. code-block:: python

   from fivedreg.base_fivedreg import FastNeuralNetwork
   import numpy as np

   # Create sample data
   X_train = np.random.randn(1000, 5)
   y_train = np.random.randn(1000)

   # Initialize model
   model = FastNeuralNetwork(
       hidden_layers=(64, 32, 16),
       learning_rate=0.001,
       max_iterations=500,
       early_stopping=True
   )

   # Train the model
   model.fit(X_train, y_train)

   # Make predictions
   X_test = np.random.randn(100, 5)
   predictions = model.predict(X_test)

Custom Configuration
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Larger architecture for complex functions
   model = FastNeuralNetwork(
       hidden_layers=(128, 64, 32),
       learning_rate=0.01,
       max_iterations=1000,
       early_stopping=True,
       verbose=True
   )

   model.fit(X_train, y_train)

   # Evaluate performance
   metrics = model.evaluate(X_test, y_test, "Test Set")
   print(f"R² Score: {metrics['r2']:.4f}")
   print(f"MAE: {metrics['mae']:.6f}")

Using Benchmark Function
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fivedreg import benchmark_training_speed

   # Train with custom hyperparameters
   model, metrics = benchmark_training_speed(
       dataset_path='my_data.pkl',
       hidden_layers=(128, 64, 32),
       learning_rate=0.001,
       max_iterations=500,
       early_stopping=True
   )

   print(f"Training completed!")
   print(f"R² Score: {metrics['r2']:.4f}")
   print(f"Training time: {metrics.get('training_time', 'N/A')}s")

Model Evaluation
~~~~~~~~~~~~~~~~

.. code-block:: python

   # Comprehensive evaluation
   metrics = model.evaluate(X_test, y_test, "Test Set")

   # Access individual metrics
   print(f"Mean Squared Error: {metrics['mse']:.6f}")
   print(f"Mean Absolute Error: {metrics['mae']:.6f}")
   print(f"Root Mean Squared Error: {metrics['rmse']:.6f}")
   print(f"R² Score: {metrics['r2']:.6f}")

Getting Model Parameters
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Get model configuration
   params = model.get_params()

   print(f"Architecture: {params['hidden_layers']}")
   print(f"Learning Rate: {params['learning_rate']}")
   print(f"Training Time: {params['training_time']:.2f}s")
   print(f"Iterations Completed: {params['iterations']}")

Dataset Format
--------------

The package expects datasets in pickle (.pkl) format with the following structure:

**Training Data**

.. code-block:: python

   {
       'X': numpy.ndarray of shape (n_samples, 5),  # 5D features
       'y': numpy.ndarray of shape (n_samples,)     # 1D targets
   }

**Prediction Data**

.. code-block:: python

   numpy.ndarray of shape (n_samples, 5)  # 5D features only

The data handler automatically:

* Validates input dimensions
* Removes NaN values
* Splits data into train (60%), validation (20%), test (20%)
* Applies standardization using StandardScaler

Performance Notes
-----------------

**Training Speed**

* 1K samples: ~5-10 seconds
* 5K samples: ~15-20 seconds
* 10K samples: ~30-50 seconds

**Accuracy**

* Typical R² scores: > 0.985
* Depends on function complexity and architecture

**Optimization Tips**

* Start with default architecture (64, 32, 16)
* Increase layers for complex functions
* Enable early_stopping to save time
* Use learning_rate between 0.0001 and 0.01

Architecture Details
--------------------

The neural network uses:

* **Activation**: ReLU (Rectified Linear Unit)
* **Solver**: Adam optimizer
* **Loss**: Mean Squared Error
* **Preprocessing**: StandardScaler for features and targets
* **Backend**: scikit-learn's MLPRegressor

Default Configuration:

* Hidden layers: (64, 32, 16)
* Learning rate: 0.001
* Max iterations: 500
* Early stopping: Enabled

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Project Information
===================

:Author: Makimona Kiakisolako (bamk3)
:Institution: University of Cambridge
:Course: DIS Course 2025
:License: MIT
:Version: 0.1.0
:Contact: bamk3@cam.ac.uk
