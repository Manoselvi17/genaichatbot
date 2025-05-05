import os
import pandas as pd
import streamlit as st

# Set relative path to the CSV
path = 'chatbot/traveldetail.csv'

# Load data
def load_data():
    if not os.path.exists(path):
        st.error(f"File not found at {path}")
        raise FileNotFoundError(f"'{path}' not found.")
    return pd.read_csv(path)

# Load and display data
df = load_data()
st.title("✈️ Travel Details Explorer")
st.success("Data loaded successfully!")

# Show raw data
if st.checkbox("Show raw data"):
    st.dataframe(df)

# Filter section
st.subheader("🔍 Filter Data")
destination = st.selectbox("Select Destination", options=["All"] + df["Destination"].unique().tolist())
transport = st.selectbox("Select Transportation Type", options=["All"] + df["Transportation type"].unique().tolist())

filtered_df = df.copy()
if destination != "All":
    filtered_df = filtered_df[filtered_df["Destination"] == destination]
if transport != "All":
    filtered_df = filtered_df[filtered_df["Transportation type"] == transport]

st.write(f"Showing {len(filtered_df)} matching records:")
st.dataframe(filtered_df)

# Stats
st.subheader("📊 Summary Statistics")
st.write(filtered_df.describe())
