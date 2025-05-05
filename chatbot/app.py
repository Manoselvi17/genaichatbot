import os
import pandas as pd
import streamlit as st

# Path where the data file should be located
path = 'traveldetail.csv'  # Update this path to where your file should be

# Display the current working directory using Streamlit
st.write(f"Current working directory: {os.getcwd()}")

# Function to load data
def load_data():
    # Check if file exists before loading
    if not os.path.exists(path):
        st.error(f"File not found at {path}")
        raise FileNotFoundError(f"'{path}' not found. Please upload it in the app directory.")
    else:
        st.write(f"File found at {path}")
        df = pd.read_csv(path)  # Replace this with your data loading logic
        return df

# Attempt to load the data and handle potential error
try:
    df = load_data()
    st.write(f"Data loaded successfully: {df.head()}")  # Display the first few rows of the data for verification
except FileNotFoundError as e:
    st.error(f"Error: {e}")
