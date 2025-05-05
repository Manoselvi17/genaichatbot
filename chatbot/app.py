import os
import pandas as pd

# Path where the data file should be located
path = 'your_file_path_here'  # Update this path to where your file should be

# Debugging: Print the current working directory to see where the app is running
print(f"Current working directory: {os.getcwd()}")

# Function to load data
def load_data():
    # Check if file exists before loading
    if not os.path.exists(path):
        print(f"File not found at {path}")
        raise FileNotFoundError(f"'{path}' not found. Please upload it in the app directory.")
    else:
        print(f"File found at {path}")
        # Replace this with your data loading logic (e.g., reading a CSV file)
        df = pd.read_csv(path)
        return df

# Attempt to load the data and handle potential error
try:
    df = load_data()
    print(f"Data loaded successfully: {df.head()}")  # Display the first few rows of the data for verification
except FileNotFoundError as e:
    print(f"Error: {e}")
