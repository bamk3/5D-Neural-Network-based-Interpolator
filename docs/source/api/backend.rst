Backend API Reference
=====================

This document provides a complete reference for the FastAPI backend REST API.

Base URL
--------

* **Development**: ``http://localhost:8000``
* **Production**: Configure via ``BACKEND_URL`` environment variable

Interactive Documentation
-------------------------

FastAPI provides automatic interactive documentation:

* **Swagger UI**: http://localhost:8000/docs
* **ReDoc**: http://localhost:8000/redoc

Health & Status Endpoints
--------------------------

GET /
~~~~~

Welcome message and service identification.

**Response:**

.. code-block:: json

   {
     "message": "Hello from the 5D Interpolator Backend by bamk3!"
   }

GET /health
~~~~~~~~~~~

Health check endpoint for monitoring and Docker containers.

**Response:**

.. code-block:: json

   {
     "status": "healthy",
     "service": "5D Interpolator Backend by bamk3"
   }

GET /status
~~~~~~~~~~~

Get the current status of uploaded data and trained models.

**Response:**

.. code-block:: json

   {
     "training_data_uploaded": true,
     "model_trained": true,
     "prediction_data_uploaded": false
   }

**Fields:**

* ``training_data_uploaded`` (boolean): Whether training dataset is loaded
* ``model_trained`` (boolean): Whether a model has been trained
* ``prediction_data_uploaded`` (boolean): Whether prediction dataset is loaded

Dataset Upload Endpoints
-------------------------

POST /upload-fit-dataset/
~~~~~~~~~~~~~~~~~~~~~~~~~~

Upload a training dataset for model fitting.

**Request:**

* **Method**: ``POST``
* **Content-Type**: ``multipart/form-data``
* **Body**: File upload with key ``file``

**File Requirements:**

* **Format**: Python pickle (``.pkl``)
* **Structure**: Dictionary with keys:

  * ``X``: NumPy array of shape ``(n, 5)`` - feature matrix
  * ``y``: NumPy array of shape ``(n,)`` - target vector

* **Validation**: Automatic shape and format checking

**Example using curl:**

.. code-block:: bash

   curl -X POST \
     http://localhost:8000/upload-fit-dataset/ \
     -F "file=@training_data.pkl"

**Success Response (200 OK):**

.. code-block:: json

   {
     "message": "Training dataset uploaded and validated successfully",
     "filename": "training_data.pkl",
     "content_type": "application/octet-stream",
     "filepath": "uploaded_datasets/training_data.pkl",
     "processing_result": "./uploaded_datasets/training_data.pkl",
     "preview": {
       "X_preview": [[1.2, -0.5, 0.9, -1.2, 0.5], ...],
       "y_preview": [3.45, 2.11, ...],
       "total_samples": 1000,
       "X_shape": [1000, 5],
       "y_shape": [1000]
     },
     "valid": true
   }

**Error Responses:**

* ``400 Bad Request``: Invalid file format or structure
* ``500 Internal Server Error``: Server error during processing

POST /upload-predict-dataset/
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Upload a prediction dataset.

**Request:**

* **Method**: ``POST``
* **Content-Type**: ``multipart/form-data``
* **Body**: File upload with key ``file``

**File Requirements:**

* **Format**: Python pickle (``.pkl``)
* **Structure**: NumPy array of shape ``(n, 5)``

**Example using curl:**

.. code-block:: bash

   curl -X POST \
     http://localhost:8000/upload-predict-dataset/ \
     -F "file=@prediction_data.pkl"

**Success Response (200 OK):**

.. code-block:: json

   {
     "message": "Prediction dataset uploaded and validated successfully",
     "filename": "prediction_data.pkl",
     "content_type": "application/octet-stream",
     "filepath": "uploaded_datasets/prediction_data.pkl",
     "predict_input": "./uploaded_datasets/prediction_data.pkl",
     "preview": {
       "X_preview": [[1.2, -0.5, 0.9, -1.2, 0.5], ...],
       "total_samples": 100,
       "X_shape": [100, 5]
     },
     "valid": true
   }

Model Training Endpoints
-------------------------

GET /hyperparameters/defaults
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get default hyperparameter values.

**Response:**

.. code-block:: json

   {
     "hidden_layer_1": 64,
     "hidden_layer_2": 32,
     "hidden_layer_3": 16,
     "learning_rate": 0.001,
     "max_iterations": 500,
     "early_stopping": true
   }

POST /start-training/
~~~~~~~~~~~~~~~~~~~~~

Train a neural network model with optional custom hyperparameters.

**Request:**

* **Method**: ``POST``
* **Content-Type**: ``application/json``
* **Body** (optional):

.. code-block:: json

   {
     "hyperparameters": {
       "hidden_layer_1": 64,
       "hidden_layer_2": 32,
       "hidden_layer_3": 16,
       "learning_rate": 0.001,
       "max_iterations": 500,
       "early_stopping": true
     }
   }

**Hyperparameter Constraints:**

* ``hidden_layer_1``: 8-256 (int)
* ``hidden_layer_2``: 8-128 (int)
* ``hidden_layer_3``: 4-64 (int)
* ``learning_rate``: 0.0001-0.01 (float)
* ``max_iterations``: 100-2000 (int)
* ``early_stopping``: true/false (boolean)

**Example using curl:**

.. code-block:: bash

   # With default hyperparameters
   curl -X POST http://localhost:8000/start-training/ \
     -H "Content-Type: application/json" \
     -d '{}'

   # With custom hyperparameters
   curl -X POST http://localhost:8000/start-training/ \
     -H "Content-Type: application/json" \
     -d '{
       "hyperparameters": {
         "hidden_layer_1": 128,
         "hidden_layer_2": 64,
         "hidden_layer_3": 32,
         "learning_rate": 0.01,
         "max_iterations": 1000,
         "early_stopping": true
       }
     }'

**Success Response (200 OK):**

.. code-block:: json

   {
     "message": "Training job initiated and completed successfully.",
     "function_result": {
       "mse": 0.0123,
       "mae": 0.0987,
       "rmse": 0.1109,
       "r2": 0.9876
     },
     "hyperparameters_used": {
       "hidden_layers": [64, 32, 16],
       "learning_rate": 0.001,
       "max_iterations": 500,
       "early_stopping": true
     }
   }

**Error Response (400 Bad Request):**

.. code-block:: json

   {
     "detail": "No training data uploaded. Please upload a dataset first."
   }

Prediction Endpoints
--------------------

POST /start-predict/
~~~~~~~~~~~~~~~~~~~~

Generate batch predictions using uploaded dataset.

**Request:**

* **Method**: ``POST``
* **Content-Type**: ``application/json``
* **Body**: ``{}`` (empty JSON object)

**Prerequisites:**

* Model must be trained
* Prediction dataset must be uploaded

**Example using curl:**

.. code-block:: bash

   curl -X POST http://localhost:8000/start-predict/ \
     -H "Content-Type: application/json" \
     -d '{}'

**Success Response (200 OK):**

.. code-block:: json

   {
     "message": "Batch prediction completed successfully.",
     "function_result": "[3.456 2.789 1.234 ...]",
     "prediction_type": "batch"
   }

POST /predict-single/
~~~~~~~~~~~~~~~~~~~~~

Generate a single prediction from 5 input features.

**Request:**

* **Method**: ``POST``
* **Content-Type**: ``application/json``
* **Body**:

.. code-block:: json

   {
     "features": [1.2, -0.5, 0.9, -1.2, 0.5]
   }

**Prerequisites:**

* Model must be trained

**Example using curl:**

.. code-block:: bash

   curl -X POST http://localhost:8000/predict-single/ \
     -H "Content-Type: application/json" \
     -d '{"features": [1.2, -0.5, 0.9, -1.2, 0.5]}'

**Success Response (200 OK):**

.. code-block:: json

   {
     "message": "Single prediction completed successfully.",
     "input_features": [1.2, -0.5, 0.9, -1.2, 0.5],
     "prediction": 3.456789,
     "prediction_type": "single"
   }

**Error Response (400 Bad Request):**

.. code-block:: json

   {
     "detail": "Expected 5 features, got 3"
   }

Python Client Examples
---------------------

Using requests library
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import requests
   import pickle
   import numpy as np

   BASE_URL = "http://localhost:8000"

   # Upload training dataset
   with open('training_data.pkl', 'rb') as f:
       response = requests.post(
           f"{BASE_URL}/upload-fit-dataset/",
           files={'file': f}
       )
   print(response.json())

   # Train model with custom hyperparameters
   response = requests.post(
       f"{BASE_URL}/start-training/",
       json={
           "hyperparameters": {
               "hidden_layer_1": 128,
               "learning_rate": 0.01,
               "max_iterations": 1000
           }
       }
   )
   print(response.json())

   # Single prediction
   response = requests.post(
       f"{BASE_URL}/predict-single/",
       json={"features": [1.2, -0.5, 0.9, -1.2, 0.5]}
   )
   print(response.json())

Error Handling
--------------

All endpoints use standard HTTP status codes:

* ``200 OK``: Successful request
* ``400 Bad Request``: Invalid input or missing prerequisites
* ``422 Unprocessable Entity``: Validation error
* ``500 Internal Server Error``: Server-side error

Error responses include a ``detail`` field with description:

.. code-block:: json

   {
     "detail": "Error description here"
   }

Rate Limiting
-------------

Currently no rate limiting is implemented. For production deployment, consider adding rate limiting middleware.

Authentication
--------------

Currently no authentication is required. For production deployment with sensitive data, implement authentication middleware.
