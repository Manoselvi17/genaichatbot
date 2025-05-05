import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier

def load_and_prepare_data(filepath):
    df = pd.read_csv(filepath)

    # Clean currency columns
    df["Accommodation cost"] = df["Accommodation cost"].replace({'\$': '', ',': '', 'USD': ''}, regex=True).astype(float)
    df["Transportation cost"] = df["Transportation cost"].replace({'\$': '', ',': '', 'USD': ''}, regex=True).astype(float)

    # Compute total cost
    df["Total cost"] = df["Accommodation cost"] + df["Transportation cost"]

    # Encode transport mode
    le = LabelEncoder()
    df["Transport_encoded"] = le.fit_transform(df["Mode of transportation"])

    # Save label encoder for later use (optional)
    with open("label_encoder.pkl", "wb") as f:
        pickle.dump(le, f)

    return df

def build_and_save_model(df):
    features = df[["Total cost", "Duration (days)", "Transport_encoded"]]
    target = df["Place"]

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    # Train model
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X_scaled, target)

    # Save model and scaler
    with open("knn_model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open("scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

def preprocess_input(total_cost, duration, transport_encoded):
    input_data = pd.DataFrame([{
        "Total cost": total_cost,
        "Duration (days)": duration,
        "Transport_encoded": transport_encoded
    }])

    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

    input_scaled = scaler.transform(input_data)
    return input_scaled
