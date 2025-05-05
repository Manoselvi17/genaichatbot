import os
import pandas as pd
import streamlit as st

# Load dataset
path = 'chatbot/traveldetail.csv'

def load_data():
    if not os.path.exists(path):
        st.error(f"File not found at {path}")
        raise FileNotFoundError(f"'{path}' not found.")
    return pd.read_csv(path)

df = load_data()

# Display available columns for verification
st.write("Available columns:", df.columns.tolist())

# Page setup
st.set_page_config(page_title="Travel Planner", layout="wide")
st.title("🌍 Smart Travel Planner")

# Sidebar inputs
st.sidebar.header("✈️ Plan Your Trip")
num_people = st.sidebar.number_input("How many people?", min_value=1, max_value=10, value=1)
num_days = st.sidebar.slider("How many days?", min_value=1, max_value=30, value=5)
budget = st.sidebar.number_input("Your total budget (USD)", min_value=100, max_value=10000, value=2000)

# Use exact column names from your CSV
accommodation_col = "Accommodation cost per person per day"
transport_col = "Transportation cost"

# Calculate total estimated cost
df["Total Estimated Cost"] = df[transport_col] + (df[accommodation_col] * num_days * num_people)

# Filter by budget
filtered_df = df[df["Total Estimated Cost"] <= budget]

# Display results
st.subheader("🧳 Trips Matching Your Preferences")
if filtered_df.empty:
    st.warning("No trips match your criteria. Try adjusting your budget or trip duration.")
else:
    st.dataframe(filtered_df[["Destination", "Transportation type", "Total Estimated Cost"]].sort_values(by="Total Estimated Cost"))

# Optional full details
with st.expander("Show full trip details"):
    st.dataframe(filtered_df)
