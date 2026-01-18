import streamlit as st
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "Data\claims_policy_merged_cleaned.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")

FEATURES = [
    "Claim_Type",
    "Estimated_Claim_Amount",
    "Traffic_Condition",
    "Weather_Condition",
    "Vehicle_Type",
    "Vehicle_Year",
    "Driver_Age",
    "Years_of_Experience"
]

TARGET = "Ultimate_Claim_Amount"

def save_model(model, feature_columns):
    os.makedirs(MODEL_DIR, exist_ok=True)

    model_path = os.path.join(MODEL_DIR, "best_model.pkl")
    feature_path = os.path.join(MODEL_DIR, "feature_columns.pkl")

    joblib.dump(model, model_path)
    joblib.dump(feature_columns, feature_path)

    return model_path, feature_path


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


def show_retraining_ui():
    st.header("Model Retraining")

    st.write("Retrain the claim amount prediction model using updated data.")

    if st.button("Retrain Model"):
        df = load_data()

        X = df[FEATURES]
        y = df[TARGET]

        X = pd.get_dummies(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        model = RandomForestRegressor(
            n_estimators=200,
            random_state=42
        )

        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        mse = mean_squared_error(y_test, preds)

        model_path, feature_path = save_model(
            model,
            X_train.columns.tolist()
        )

        st.success("Model retraining completed")
        st.write("Mean Squared Error:", round(mse, 2))
        st.write("Saved model:", model_path)
        st.write("Saved features:", feature_path)
