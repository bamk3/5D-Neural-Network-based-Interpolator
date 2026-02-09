Neural Network Module
=====================

Complete API reference for the ``fivedreg`` neural network package, automatically generated from source code docstrings.

Module Overview
---------------

.. automodule:: fivedreg.base_fivedreg
   :no-members:

FastNeuralNetwork Class
-----------------------

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
-------------------

benchmark_training_speed
~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: fivedreg.base_fivedreg.benchmark_training_speed

start_predict
~~~~~~~~~~~~~

.. autofunction:: fivedreg.base_fivedreg.start_predict

demonstrate_configurability
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: fivedreg.base_fivedreg.demonstrate_configurability

Data Handling Module
--------------------

.. automodule:: fivedreg.data_hand.module
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Basic Training
~~~~~~~~~~~~~~

.. code-block:: python

   from fivedreg.base_fivedreg import FastNeuralNetwork

   # Create model with default configuration
   model = FastNeuralNetwork(
       hidden_layers=(64, 32, 16),
       learning_rate=0.001,
       max_iterations=500
   )

   # Train the model
   model.fit(X_train, y_train)

   # Make predictions
   predictions = model.predict(X_test)

Custom Configuration
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Create model with custom architecture
   model = FastNeuralNetwork(
       hidden_layers=(128, 64, 32),
       learning_rate=0.01,
       max_iterations=1000,
       early_stopping=True,
       verbose=True
   )

   # Train and evaluate
   model.fit(X_train, y_train)
   metrics = model.evaluate(X_test, y_test, "Test")

   print(f"R² Score: {metrics['r2']:.4f}")
   print(f"MAE: {metrics['mae']:.6f}")

Using Benchmark Function
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fivedreg.base_fivedreg import benchmark_training_speed

   # Train with custom hyperparameters
   model, metrics = benchmark_training_speed(
       dataset_path='data.pkl',
       hidden_layers=(128, 64, 32),
       learning_rate=0.001,
       max_iterations=500,
       early_stopping=True
   )

   print(f"Training completed!")
   print(f"R² Score: {metrics['r2']:.4f}")

Making Predictions
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fivedreg.base_fivedreg import start_predict
   import numpy as np

   # Load prediction data
   X_new = np.random.randn(100, 5)

   # Make predictions (requires model to be trained first via benchmark_training_speed)
   predictions = start_predict(X_new)

Model Evaluation
~~~~~~~~~~~~~~~~

.. code-block:: python

   # Evaluate on test set
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

See Also
--------

* :doc:`backend` - Backend API reference
* :doc:`frontend` - Frontend components
* :doc:`../usage` - Usage guide
* :doc:`../performance` - Performance benchmarks
