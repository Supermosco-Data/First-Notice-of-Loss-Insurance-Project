import pandas as pd
import joblib
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from datetime import datetime
from huggingface_hub import hf_hub_download


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
REPO_ID = "SUPERMOSCO/fnol_model"
MODEL_FILENAME = "best_model.pkl"
FEATURE_FILENAME = "feature_columns.pkl"

def load_model():
    model_file = hf_hub_download(
        repo_id = REPO_ID,
        filename = MODEL_FILENAME
    )
    feature_file = hf_hub_download(
        repo_id = REPO_ID,
        filename = FEATURE_FILENAME
    )

    model = joblib.load(model_file)
    feature_columns = joblib.load(feature_file)

    return model, feature_columns
    

def save_model(model, feature_columns, versioned=False):
    os.makedirs(MODEL_DIR, exist_ok=True)

    if versioned:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_path = os.path.join(MODEL_DIR, f"model_{timestamp}.pkl")
        feature_path = os.path.join(MODEL_DIR, f"features_{timestamp}.pkl")
    else:
        model_path = os.path.join(MODEL_DIR, MODEL_FILENAME)
        feature_path = os.path.join(MODEL_DIR, FEATURE_FILENAME)

    joblib.dump(model, model_path)
    joblib.dump(feature_columns, feature_path)

    return model_path, feature_path


