import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import joblib

def load_and_prepare_data(csv_path="traveldetail.csv"):
    # Load data from CSV
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()  # Remove extra spaces from column names
    df.dropna(subset=["Accommodation cost", "Transportation cost", "Duration (days)", "Transportation type"], inplace=True)  # Drop rows with missing important columns
    
    # Remove any non-numeric characters (currency symbols and text)
    df["Accommodation cost"] = df["Accommodation cost"].replace({'\$': '', ',': '', 'USD': ''}, regex=True).astype(float)
    df["Transportation cost"] = df["Transportation cost"].replace({'\$': '', ',': '', 'USD': ''}, regex=True).astype(float)
    
    # Create new column for total cost
    df["Total cost"] = df["Accommodation cost"] + df["Transportation cost"]
    
    # Encode transportation type as numerical values
    df["Transport_encoded"] = df["Transportation type"].astype('category').cat.codes
    return df

def build_and_save_model(df, model_path="knn_model.pkl", scaler_path="scaler.pkl"):
    # Prepare features (Total cost, Duration, Transport_encoded)
    features = df[["Total cost", "Duration (days)", "Transport_encoded"]]
    
    # Check for missing values in the features
    if features.isnull().sum().sum() > 0:
        print("🚨 Missing data detected in features!")
        features = features.dropna()  # Drop rows with missing values
        # Alternatively, you could fill missing values: features = features.fillna(0)
    else:
        print("✅ No missing data in features.")
    
    # Print preview of features data
    print("Features data preview:")
    print(features.head())

    # Scale the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)
    
    # Initialize and train the KNN model
    knn = NearestNeighbors(n_neighbors=3)
    knn.fit(X_scaled)
    
    # Save the trained model and scaler to files
    joblib.dump(knn, model_path)
    joblib.dump(scaler, scaler_path)
    
    print("✅ Model and scaler saved successfully!")
    return knn, scaler

def load_model(model_path="knn_model.pkl", scaler_path="scaler.pkl"):
    # Load the trained KNN model and scaler
    knn = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return knn, scaler

def recommend_trips(df, knn, scaler, budget, duration, transport):
    # Find the encoded value for the transport type
    transport_code = df[df["Transportation type"] == transport]["Transport_encoded"].iloc[0]
    
    # Prepare user input for prediction
    user_input = pd.DataFrame([[budget, duration, transport_code]], columns=["Total cost", "Duration (days)", "Transport_encoded"])
    
    # Scale the user input
    user_scaled = scaler.transform(user_input)
    
    # Find the closest trips using KNN
    distances, indices = knn.kneighbors(user_scaled)
    
    # Return the recommended trips
    return df.iloc[indices[0]][["Destination", "Accommodation type", "Transportation type", "Total cost", "Duration (days)"]]
