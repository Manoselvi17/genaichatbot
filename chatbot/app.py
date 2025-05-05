import streamlit as st
import pandas as pd
import os
import pickle
from model import preprocess_input

# 🔽 Add the load_data function here
def load_data():
    path = "traveldetail.csv"
    if not os.path.exists(path):
        raise FileNotFoundError(f"'{path}' not found. Please make sure it is in the app directory.")
    return pd.read_csv(path)

# 🔽 Load the CSV using the new function
df = load_data()

# Example Streamlit UI (expand this as needed)
st.title("Travel Cost Predictor")

duration = st.number_input("Enter duration (days):", min_value=1)
transport = st.selectbox("Select transportation mode:", df["Transport"].unique())

if st.button("Predict Cost"):
    user_input = {
        "Duration (days)": duration,
        "Transport": transport
    }
    input_df = preprocess_input(pd.DataFrame([user_input]), df)

    # Load model and scaler
    with open("knn_model.pkl", "rb") as model_file:
        model = pickle.load(model_file)
    with open("scaler.pkl", "rb") as scaler_file:
        scaler = pickle.load(scaler_file)

    input_scaled = scaler.transform(input_df)
    prediction = model.predict(input_scaled)
    st.success(f"Estimated total cost: ${prediction[0]:,.2f}")
