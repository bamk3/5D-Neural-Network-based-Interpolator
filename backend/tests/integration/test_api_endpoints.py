"""
Integration tests for FastAPI endpoints
"""

import pytest
import io
import pickle
import numpy as np
from fastapi.testclient import TestClient
from pathlib import Path
import os


@pytest.mark.integration
@pytest.mark.api
class TestHealthEndpoints:
    """Test health check endpoints"""

    def test_root_endpoint(self, test_client):
        """Test GET / endpoint"""
        response = test_client.get("/")

        assert response.status_code == 200
        assert "message" in response.json()
        assert "5D Interpolator" in response.json()["message"]

    def test_health_endpoint(self, test_client):
        """Test GET /health endpoint"""
        response = test_client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "service" in data

    def test_status_endpoint_initial(self, test_client, reset_global_state):
        """Test GET /status endpoint with no data uploaded"""
        response = test_client.get("/status")

        assert response.status_code == 200
        data = response.json()
        assert "training_data_uploaded" in data
        assert "model_trained" in data
        assert "prediction_data_uploaded" in data

        # Initially all should be False
        assert data["training_data_uploaded"] is False
        assert data["model_trained"] is False
        assert data["prediction_data_uploaded"] is False


@pytest.mark.integration
@pytest.mark.api
class TestUploadFitDataset:
    """Test POST /upload-fit-dataset/ endpoint"""

    def test_upload_valid_dataset(self, test_client, sample_data_small, uploaded_datasets_dir, reset_global_state):
        """Test uploading a valid training dataset"""
        # Create file-like object
        pkl_data = pickle.dumps(sample_data_small)
        files = {"file": ("test_train.pkl", io.BytesIO(pkl_data), "application/octet-stream")}

        response = test_client.post("/upload-fit-dataset/", files=files)

        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert "success" in data["message"].lower()
        assert data["valid"] is True
        assert data["filename"] == "test_train.pkl"
        assert "preview" in data
        assert data["preview"]["total_samples"] == 100
        assert data["preview"]["X_shape"] == [100, 5]
        assert data["preview"]["y_shape"] == [100]

    def test_upload_invalid_file_type(self, test_client, reset_global_state):
        """Test uploading non-.pkl file"""
        files = {"file": ("test.txt", io.BytesIO(b"not a pickle file"), "text/plain")}

        response = test_client.post("/upload-fit-dataset/", files=files)

        assert response.status_code == 400
        assert "Invalid file type" in response.json()["detail"]

    def test_upload_invalid_X_shape(self, test_client, reset_global_state):
        """Test uploading dataset with wrong X shape"""
        invalid_data = {'X': np.random.randn(10, 3), 'y': np.random.randn(10)}
        pkl_data = pickle.dumps(invalid_data)
        files = {"file": ("invalid.pkl", io.BytesIO(pkl_data), "application/octet-stream")}

        response = test_client.post("/upload-fit-dataset/", files=files)

        assert response.status_code == 400
        assert "Invalid format" in response.json()["detail"]
        assert "shape (n, 5)" in response.json()["detail"]

    def test_upload_invalid_y_shape(self, test_client, reset_global_state):
        """Test uploading dataset with wrong y shape"""
        invalid_data = {'X': np.random.randn(10, 5), 'y': np.random.randn(10, 2)}
        pkl_data = pickle.dumps(invalid_data)
        files = {"file": ("invalid.pkl", io.BytesIO(pkl_data), "application/octet-stream")}

        response = test_client.post("/upload-fit-dataset/", files=files)

        assert response.status_code == 400
        assert "Invalid format" in response.json()["detail"]
        assert "1-dimensional" in response.json()["detail"]

    def test_upload_mismatched_samples(self, test_client, reset_global_state):
        """Test uploading dataset with mismatched X and y samples"""
        invalid_data = {'X': np.random.randn(10, 5), 'y': np.random.randn(15)}
        pkl_data = pickle.dumps(invalid_data)
        files = {"file": ("invalid.pkl", io.BytesIO(pkl_data), "application/octet-stream")}

        response = test_client.post("/upload-fit-dataset/", files=files)

        assert response.status_code == 400
        assert "same number of samples" in response.json()["detail"]

    def test_upload_missing_keys(self, test_client, reset_global_state):
        """Test uploading dataset without required keys"""
        invalid_data = {'X': np.random.randn(10, 5)}  # Missing 'y'
        pkl_data = pickle.dumps(invalid_data)
        files = {"file": ("invalid.pkl", io.BytesIO(pkl_data), "application/octet-stream")}

        response = test_client.post("/upload-fit-dataset/", files=files)

        assert response.status_code == 400
        assert "'X' and 'y' keys" in response.json()["detail"]

    def test_upload_not_dict(self, test_client, reset_global_state):
        """Test uploading non-dictionary data"""
        invalid_data = np.random.randn(10, 5)
        pkl_data = pickle.dumps(invalid_data)
        files = {"file": ("invalid.pkl", io.BytesIO(pkl_data), "application/octet-stream")}

        response = test_client.post("/upload-fit-dataset/", files=files)

        assert response.status_code == 400
        assert "dictionary" in response.json()["detail"].lower()

    def test_upload_creates_file(self, test_client, sample_data_small, uploaded_datasets_dir, reset_global_state):
        """Test that upload creates file in uploaded_datasets directory"""
        pkl_data = pickle.dumps(sample_data_small)
        files = {"file": ("test_create.pkl", io.BytesIO(pkl_data), "application/octet-stream")}

        response = test_client.post("/upload-fit-dataset/", files=files)

        assert response.status_code == 200

        # Check file exists
        file_path = os.path.join(uploaded_datasets_dir, "test_create.pkl")
        assert os.path.exists(file_path)

    def test_upload_invalid_removes_file(self, test_client, uploaded_datasets_dir, reset_global_state):
        """Test that invalid upload removes the created file"""
        invalid_data = {'X': np.random.randn(10, 3), 'y': np.random.randn(10)}
        pkl_data = pickle.dumps(invalid_data)
        files = {"file": ("test_invalid.pkl", io.BytesIO(pkl_data), "application/octet-stream")}

        response = test_client.post("/upload-fit-dataset/", files=files)

        assert response.status_code == 400

        # File should not exist
        file_path = os.path.join(uploaded_datasets_dir, "test_invalid.pkl")
        assert not os.path.exists(file_path)


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.slow
class TestTraining:
    """Test POST /start-training/ endpoint"""

    def test_training_with_valid_data(self, test_client, sample_data_medium, uploaded_datasets_dir, reset_global_state):
        """Test successful training flow"""
        # First upload dataset
        pkl_data = pickle.dumps(sample_data_medium)
        files = {"file": ("train_data.pkl", io.BytesIO(pkl_data), "application/octet-stream")}

        upload_response = test_client.post("/upload-fit-dataset/", files=files)
        assert upload_response.status_code == 200

        # Then start training
        train_response = test_client.post("/start-training/")

        assert train_response.status_code == 200
        data = train_response.json()

        assert "message" in data
        assert "success" in data["message"].lower()
        assert "function_result" in data

        # Check metrics
        metrics = data["function_result"]
        assert "mse" in metrics
        assert "mae" in metrics
        assert "rmse" in metrics
        assert "r2" in metrics

    def test_training_updates_status(self, test_client, sample_data_medium, uploaded_datasets_dir, reset_global_state):
        """Test that training updates the status endpoint"""
        # Upload and train
        pkl_data = pickle.dumps(sample_data_medium)
        files = {"file": ("train_status.pkl", io.BytesIO(pkl_data), "application/octet-stream")}

        test_client.post("/upload-fit-dataset/", files=files)
        test_client.post("/start-training/")

        # Check status
        status_response = test_client.get("/status")
        data = status_response.json()

        assert data["training_data_uploaded"] is True
        assert data["model_trained"] is True


@pytest.mark.integration
@pytest.mark.api
class TestUploadPredictDataset:
    """Test POST /upload-predict-dataset/ endpoint"""

    def test_upload_valid_predict_data(self, test_client, uploaded_datasets_dir, reset_global_state):
        """Test uploading valid prediction dataset"""
        X_pred = np.random.randn(20, 5)
        pkl_data = pickle.dumps(X_pred)
        files = {"file": ("predict.pkl", io.BytesIO(pkl_data), "application/octet-stream")}

        response = test_client.post("/upload-predict-dataset/", files=files)

        assert response.status_code == 200
        data = response.json()

        assert data["valid"] is True
        assert data["preview"]["total_samples"] == 20
        assert data["preview"]["X_shape"] == [20, 5]

    def test_upload_invalid_predict_shape(self, test_client, reset_global_state):
        """Test uploading prediction data with wrong shape"""
        X_pred = np.random.randn(20, 3)  # Wrong number of features
        pkl_data = pickle.dumps(X_pred)
        files = {"file": ("predict_invalid.pkl", io.BytesIO(pkl_data), "application/octet-stream")}

        response = test_client.post("/upload-predict-dataset/", files=files)

        assert response.status_code == 400
        assert "shape (n, 5)" in response.json()["detail"]

    def test_upload_predict_non_pkl(self, test_client, reset_global_state):
        """Test uploading non-.pkl file for prediction"""
        files = {"file": ("predict.txt", io.BytesIO(b"not a pickle"), "text/plain")}

        response = test_client.post("/upload-predict-dataset/", files=files)

        assert response.status_code == 400
        assert "Invalid file type" in response.json()["detail"]


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.slow
class TestPrediction:
    """Test prediction endpoints"""

    def test_batch_predict_without_model(self, test_client, reset_global_state):
        """Test batch prediction without training model first"""
        # Upload prediction data
        X_pred = np.random.randn(10, 5)
        pkl_data = pickle.dumps(X_pred)
        files = {"file": ("predict.pkl", io.BytesIO(pkl_data), "application/octet-stream")}
        test_client.post("/upload-predict-dataset/", files=files)

        # Try to predict without model
        response = test_client.post("/start-predict/")

        assert response.status_code == 400
        assert "No trained model" in response.json()["detail"]

    def test_batch_predict_without_data(self, test_client, sample_data_medium, uploaded_datasets_dir, reset_global_state):
        """Test batch prediction without uploading prediction data"""
        # Upload and train model
        pkl_data = pickle.dumps(sample_data_medium)
        files = {"file": ("train.pkl", io.BytesIO(pkl_data), "application/octet-stream")}
        test_client.post("/upload-fit-dataset/", files=files)
        test_client.post("/start-training/")

        # Try to predict without prediction data
        response = test_client.post("/start-predict/")

        assert response.status_code == 400
        assert "No prediction data" in response.json()["detail"]

    def test_batch_predict_success(self, test_client, sample_data_medium, uploaded_datasets_dir, reset_global_state):
        """Test successful batch prediction"""
        # Upload and train
        pkl_data = pickle.dumps(sample_data_medium)
        files = {"file": ("train.pkl", io.BytesIO(pkl_data), "application/octet-stream")}
        test_client.post("/upload-fit-dataset/", files=files)
        test_client.post("/start-training/")

        # Upload prediction data
        X_pred = np.random.randn(15, 5)
        pred_pkl = pickle.dumps(X_pred)
        pred_files = {"file": ("predict.pkl", io.BytesIO(pred_pkl), "application/octet-stream")}
        test_client.post("/upload-predict-dataset/", files=pred_files)

        # Make predictions
        response = test_client.post("/start-predict/")

        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert "success" in data["message"].lower()
        assert "function_result" in data
        assert data["prediction_type"] == "batch"

    def test_single_predict_without_model(self, test_client, reset_global_state):
        """Test single prediction without model"""
        response = test_client.post(
            "/predict-single/",
            json={"features": [1.0, 2.0, 3.0, 4.0, 5.0]}
        )

        assert response.status_code == 400
        assert "No trained model" in response.json()["detail"]

    def test_single_predict_wrong_feature_count(self, test_client, sample_data_medium, uploaded_datasets_dir, reset_global_state):
        """Test single prediction with wrong number of features"""
        # Upload and train
        pkl_data = pickle.dumps(sample_data_medium)
        files = {"file": ("train.pkl", io.BytesIO(pkl_data), "application/octet-stream")}
        test_client.post("/upload-fit-dataset/", files=files)
        test_client.post("/start-training/")

        # Try with wrong number of features
        response = test_client.post(
            "/predict-single/",
            json={"features": [1.0, 2.0, 3.0]}  # Only 3 features
        )

        assert response.status_code == 400
        assert "Expected 5 features" in response.json()["detail"]

    def test_single_predict_success(self, test_client, sample_data_medium, uploaded_datasets_dir, reset_global_state):
        """Test successful single prediction"""
        # Upload and train
        pkl_data = pickle.dumps(sample_data_medium)
        files = {"file": ("train.pkl", io.BytesIO(pkl_data), "application/octet-stream")}
        test_client.post("/upload-fit-dataset/", files=files)
        test_client.post("/start-training/")

        # Make single prediction
        response = test_client.post(
            "/predict-single/",
            json={"features": [1.0, 2.0, 3.0, 4.0, 5.0]}
        )

        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert "success" in data["message"].lower()
        assert "prediction" in data
        assert "input_features" in data
        assert data["prediction_type"] == "single"
        assert isinstance(data["prediction"], float)
        assert data["input_features"] == [1.0, 2.0, 3.0, 4.0, 5.0]


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.slow
class TestEndToEndWorkflow:
    """Test complete end-to-end workflow"""

    def test_complete_workflow(self, test_client, sample_data_medium, uploaded_datasets_dir, reset_global_state):
        """Test complete workflow: upload -> train -> predict"""
        # 1. Check initial status
        status = test_client.get("/status").json()
        assert status["training_data_uploaded"] is False
        assert status["model_trained"] is False

        # 2. Upload training dataset
        pkl_data = pickle.dumps(sample_data_medium)
        files = {"file": ("workflow_train.pkl", io.BytesIO(pkl_data), "application/octet-stream")}
        upload_response = test_client.post("/upload-fit-dataset/", files=files)
        assert upload_response.status_code == 200

        # 3. Check status after upload
        status = test_client.get("/status").json()
        assert status["training_data_uploaded"] is True
        assert status["model_trained"] is False

        # 4. Train model
        train_response = test_client.post("/start-training/")
        assert train_response.status_code == 200
        metrics = train_response.json()["function_result"]
        assert metrics["r2"] > 0.9  # Should achieve good fit

        # 5. Check status after training
        status = test_client.get("/status").json()
        assert status["model_trained"] is True

        # 6. Upload prediction data
        X_pred = np.random.randn(10, 5)
        pred_pkl = pickle.dumps(X_pred)
        pred_files = {"file": ("workflow_pred.pkl", io.BytesIO(pred_pkl), "application/octet-stream")}
        pred_upload_response = test_client.post("/upload-predict-dataset/", files=pred_files)
        assert pred_upload_response.status_code == 200

        # 7. Make batch predictions
        batch_pred_response = test_client.post("/start-predict/")
        assert batch_pred_response.status_code == 200

        # 8. Make single prediction
        single_pred_response = test_client.post(
            "/predict-single/",
            json={"features": [0.5, -0.5, 1.0, -1.0, 0.0]}
        )
        assert single_pred_response.status_code == 200
        assert isinstance(single_pred_response.json()["prediction"], float)
