#main.py pour le backend


import pickle
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # The use 'Agg' backend is recommended for non-GUI environments
import os
import shutil
from typing import Dict, List, Optional, Any
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
from fivedreg import benchmark_training_speed



app = FastAPI(
    title="5D Interpolator by bamk3",
    description="Neural network-based 5D function interpolator developped by Makimona Kiakisolako (bamk3) as part of the C1 DIS course at the University of Cambridge.",
    version="0.1.0",
    contact={"name": "Makimona Kiakisolako", "email": "bamk3@cam.ac.uk"},
    license_info={"name": "MIT"},)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # This is the link to my frontend React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)


class Item(BaseModel):

    """
    Here I define a Pydantic model. It is closely related to what we did in class as the ssential of the code here has been taken from the FastAPI documentation used in C1 lectures.
    """
    name: str
    price: float


@app.get("/")
def hello():
    return {"message": "Hello from the 5D Interpolator Backend by bamk3!"}

@app.get("/health")
def health_check():
    """Health check endpoint for Docker containers"""
    return {"status": "healthy", "service": "5D Interpolator Backend by bamk3"}

@app.get("/status")
def get_status():
    """Get the current status of the system"""
    return {
        "training_data_uploaded": 'processing_result' in globals() and processing_result is not None,
        "model_trained": 'train_result' in globals() and train_result is not None,
        "prediction_data_uploaded": 'predict_input' in globals() and predict_input is not None
    }

@app.post("/reset")
def reset_state():
    """
    Reset all global state (trained model and uploaded datasets).
    This allows users to start fresh with a new dataset.
    """
    global processing_result, train_result, predict_input

    # Clear global variables
    processing_result = None
    train_result = None
    predict_input = None

    # Optionally clear uploaded files
    if os.path.exists(UPLOAD_DIRECTORY):
        for file in os.listdir(UPLOAD_DIRECTORY):
            file_path = os.path.join(UPLOAD_DIRECTORY, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

    return {
        "message": "System reset successfully. All previous data and models cleared.",
        "status": "reset_complete"
    }


# Configuration for where I'll save the files (I made sure that this directory exists)
UPLOAD_DIRECTORY = "uploaded_datasets"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@app.post("/upload-fit-dataset/")
async def upload_fit_dataset(
    
    file: UploadFile = File(..., description="The dataset file to upload (.pkl format).")):
    """
    This Post endpoint accepts a training dataset file upload, validates format, and saves it to the specified directory.
    Expected format: Dict with 'X' (n,5) and 'y' (n,) arrays
    """

    # Here, I define the path where the file will be saved.
    # The 'filename' attribute will come from the client's submitted form data.
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)

    # Use a context manager and shutil.copyfileobj for efficient file streaming
  
    if str(file_path)[-3:] == 'pkl':
        global processing_result
        processing_result = './' + str(file_path)
        try:
            with open(file_path, "wb") as buffer:
            # This copies the file content in chunks, suitable for large files
                shutil.copyfileobj(file.file, buffer)

            # Validate the uploaded data
            try:
                data = pickle.load(open(file_path, "rb"))

                # Check if data is a dictionary with 'X' and 'y' keys
                if not isinstance(data, dict):
                    raise HTTPException(status_code=400, detail="Invalid format: Data must be a dictionary with 'X' and 'y' keys")

                if 'X' not in data or 'y' not in data:
                    raise HTTPException(status_code=400, detail="Invalid format: Dictionary must contain 'X' and 'y' keys")

                X = np.array(data['X'])
                y = np.array(data['y'])

                # Check dimensions
                if len(X.shape) != 2 or X.shape[1] != 5:
                    raise HTTPException(status_code=400, detail=f"Invalid format: X must have shape (n, 5), got {X.shape}")

                if len(y.shape) != 1:
                    raise HTTPException(status_code=400, detail=f"Invalid format: y must be 1-dimensional, got shape {y.shape}")

                if X.shape[0] != y.shape[0]:
                    raise HTTPException(status_code=400, detail=f"Invalid format: X and y must have same number of samples. X: {X.shape[0]}, y: {y.shape[0]}")

                # Create preview (first 5 rows)
                preview_size = min(5, X.shape[0])
                preview_data = {
                    "X_preview": X[:preview_size].tolist(),
                    "y_preview": y[:preview_size].tolist(),
                    "total_samples": X.shape[0],
                    "X_shape": X.shape,
                    "y_shape": y.shape
                }

                return {
                    "message": "Training dataset uploaded and validated successfully",
                    "filename": file.filename,
                    "content_type": file.content_type,
                    "filepath": file_path,
                    "processing_result": processing_result,
                    "preview": preview_data,
                    "valid": True
                }

            except HTTPException as he:
                # Remove invalid file
                if os.path.exists(file_path):
                    os.remove(file_path)
                raise he
            except Exception as e:
                # Remove file if validation fails
                if os.path.exists(file_path):
                    os.remove(file_path)
                raise HTTPException(status_code=400, detail=f"Error validating file: {str(e)}")

        except HTTPException:
            raise
        except Exception as e:
            # Handle potential errors during file handling
            raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")
        finally:
            # Close the UploadFile object's underlying file handle
            await file.close()
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .pkl file.")


# Define the Pydantic input model (Schema)
class HyperparametersConfig(BaseModel):
    """
    This is a schema for neural network hyperparameters configuration.
    """
    hidden_layer_1: int = Field(default=64, ge=8, le=256, description="Neurons in first hidden layer")
    hidden_layer_2: int = Field(default=32, ge=8, le=128, description="Neurons in second hidden layer")
    hidden_layer_3: int = Field(default=16, ge=4, le=64, description="Neurons in third hidden layer")
    learning_rate: float = Field(default=0.001, ge=0.0001, le=0.01, description="Learning rate")
    max_iterations: int = Field(default=500, ge=100, le=2000, description="Maximum training iterations")
    early_stopping: bool = Field(default=True, description="Enable early stopping")

class TrainRequest(BaseModel):
    """
     This is a schema for the POST request body with hyperparameters.
    """
    hyperparameters: Optional[HyperparametersConfig] = Field(default=None, description="Model hyperparameters")


@app.get("/hyperparameters/defaults")
def get_default_hyperparameters():
    """
    Here I define default hyperparameter values from the example given in the coursework instructions.
    """
    return {
        "hidden_layer_1": 64,
        "hidden_layer_2": 32,
        "hidden_layer_3": 16,
        "learning_rate": 0.001,
        "max_iterations": 500,
        "early_stopping": True
    }


# Training Endpoint
@app.post("/start-training/", response_model=Dict[str, Any])
def start_training(request: TrainRequest = TrainRequest()):
    """
    Trigger model training with configurable hyperparameters.
    Accept optional hyperparameters in the request body.
    """

    # Check if training data has been uploaded
    if 'processing_result' not in globals() or processing_result is None:
        raise HTTPException(
            status_code=400,
            detail="No training dataset uploaded. Please upload a training dataset first using /upload-fit-dataset/"
        )

    # Verify the dataset file still exists
    if not os.path.exists(processing_result):
        raise HTTPException(
            status_code=400,
            detail=f"Training dataset file not found at {processing_result}. Please upload the dataset again."
        )

    # Extract hyperparameters or use defaults
    if request.hyperparameters:
        hyperparams = request.hyperparameters
        hidden_layers = (
            hyperparams.hidden_layer_1,
            hyperparams.hidden_layer_2,
            hyperparams.hidden_layer_3
        )
        learning_rate = hyperparams.learning_rate
        max_iterations = hyperparams.max_iterations
        early_stopping = hyperparams.early_stopping
    else:
        # Use defaults
        hidden_layers = (64, 32, 16)
        learning_rate = 0.001
        max_iterations = 500
        early_stopping = True

    # Call training function with hyperparameters
    try:
        global train_result
        train_result = benchmark_training_speed(
            processing_result,
            hidden_layers=hidden_layers,
            learning_rate=learning_rate,
            max_iterations=max_iterations,
            early_stopping=early_stopping
        )

        # Return the result with hyperparameters used
        return {
            "message": "Training job initiated and completed successfully.",
            "function_result": train_result[1],
            "hyperparameters_used": {
                "hidden_layers": hidden_layers,
                "learning_rate": learning_rate,
                "max_iterations": max_iterations,
                "early_stopping": early_stopping
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")


@app.post("/upload-predict-dataset/")
async def upload_predict_dataset(
   
    file: UploadFile = File(..., description="The dataset file to upload (.pkl format).")):
    """
    This function accepts a prediction dataset file upload, validates format, and saves it to the specified directory.
    Expected format: Array with shape (n, 5)
    """

    # The path where the file will be saved
    # The 'filename' attribute comes from the client's submitted form data
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)

    # Here we use a context manager and shutil.copyfileobj for efficient file streaming
    # 'file.file' is the SpooledTemporaryFile object
    if str(file_path)[-3:] == 'pkl':
        global predict_input
        predict_input = './' + str(file_path)
        try:
            with open(file_path, "wb") as buffer:
            # This copies the file content in chunks, suitable for large files
                shutil.copyfileobj(file.file, buffer)

            # Validate the uploaded data
            try:
                data = pickle.load(open(file_path, "rb"))

                # Convert to numpy array
                X_pred = np.array(data)

                # Check dimensions
                if len(X_pred.shape) != 2 or X_pred.shape[1] != 5:
                    raise HTTPException(status_code=400, detail=f"Invalid format: Prediction data must have shape (n, 5), got {X_pred.shape}")

                # Create preview (first 5 rows)
                preview_size = min(5, X_pred.shape[0])
                preview_data = {
                    "X_preview": X_pred[:preview_size].tolist(),
                    "total_samples": X_pred.shape[0],
                    "X_shape": X_pred.shape
                }

                return {
                    "message": "Prediction dataset uploaded and validated successfully",
                    "filename": file.filename,
                    "content_type": file.content_type,
                    "filepath": file_path,
                    "predict_input": predict_input,
                    "preview": preview_data,
                    "valid": True
                }

            except HTTPException as he:
                # Remove invalid file
                if os.path.exists(file_path):
                    os.remove(file_path)
                raise he
            except Exception as e:
                # Remove file if validation fails
                if os.path.exists(file_path):
                    os.remove(file_path)
                raise HTTPException(status_code=400, detail=f"Error validating file: {str(e)}")

        except HTTPException:
            raise
        except Exception as e:
        # Handle potential errors during file handling
            raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")
        finally:
        # Close the UploadFile object's underlying file handle
            await file.close()
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .pkl file.")


# Defining the Pydantic input model (Schema)
class TrainRequest(BaseModel):
    """
    Schema for the POST request body.
    We use 'param' as a generic name for the input value.
    """
    param: Any = Field()

class SinglePredictionRequest(BaseModel):
    """
    Schema for single prediction request with 5 features.
    """
    features: List[float]

@app.post("/start-predict/", response_model=Dict[str, Any])
def predict_batch():
    """
    Perform batch prediction using uploaded dataset.
    For this, the user only needs to send a simple POST request (e.g., via a button click) and no request body data is required.
    """

    try:
        if 'train_result' not in globals() or train_result is None:
            raise HTTPException(status_code=400, detail="No trained model available. Please train a model first.")

        if 'predict_input' not in globals() or predict_input is None:
            raise HTTPException(status_code=400, detail="No prediction data uploaded. Please upload a prediction dataset first.")

        predicted_result = train_result[0].predict(pickle.load(open(predict_input, "rb")))

        # Return the result of the function call
        return {
            "message": "Batch prediction completed successfully.",
            "function_result": str(predicted_result),
            "prediction_type": "batch"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")

@app.post("/predict-single/", response_model=Dict[str, Any])
def predict_single(request: SinglePredictionRequest):
    """
    Performs single prediction with 5 input features.
    """

    try:
        if 'train_result' not in globals() or train_result is None:
            raise HTTPException(status_code=400, detail="No trained model available. Please train a model first.")

        # Validate that we have exactly 5 features
        if len(request.features) != 5:
            raise HTTPException(status_code=400, detail=f"Expected 5 features, got {len(request.features)}")

        # Convert to numpy array and reshape for prediction
        input_array = np.array([request.features])

        # Make prediction
        predicted_result = train_result[0].predict(input_array)

        return {
            "message": "Single prediction completed successfully.",
            "input_features": request.features,
            "prediction": float(predicted_result[0]),
            "prediction_type": "single"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")