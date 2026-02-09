import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_dataset(filepath):
    """
    This module helps in loading and preprocessing 5D datasets. It reads data from a pickle file,
    removes NaN values, splits the data into training, validation, and test sets, and standardizes the features and target variable.

    Returns:
        Tuple of (X_train, y_train, X_val, y_val, X_test, y_test, scaler_X, scaler_y)

        We can notice that it returns everything needed for training and evaluating a regression model.
    """
    data_dict = pickle.load(open(filepath, "rb"))

    # Validate input shape
    if data_dict['X'].shape[1] != 5 or data_dict['y'].ndim != 1:
        raise ValueError(f"Expected X with 5 features and 1D y, got X: {data_dict['X'].shape}, y: {data_dict['y'].shape}")

    X = data_dict['X']
    y = data_dict['y']

    # Remove NaN values
    valid_mask = ~(np.isnan(X).any(axis=1) | np.isnan(y))
    X = X[valid_mask]
    y = y[valid_mask]

    print(f"Dataset: {X.shape[0]} samples, 5 features")
    print(f"Target range: [{y.min():.4f}, {y.max():.4f}]")

    # Split: 60% train, 20% val, 20% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.25, random_state=42
    )

    # Standardize
    scaler_X = StandardScaler()
    scaler_y = StandardScaler()

    X_train = scaler_X.fit_transform(X_train)
    y_train = scaler_y.fit_transform(y_train.reshape(-1, 1)).flatten()

    X_val = scaler_X.transform(X_val)
    y_val = scaler_y.transform(y_val.reshape(-1, 1)).flatten()

    X_test = scaler_X.transform(X_test)
    y_test = scaler_y.transform(y_test.reshape(-1, 1)).flatten()

    print(f"Split: Train={len(X_train)}, Val={len(X_val)}, Test={len(X_test)}")

    return X_train, y_train, X_val, y_val, X_test, y_test, scaler_X, scaler_y