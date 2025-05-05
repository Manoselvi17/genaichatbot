import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("traveldetail.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

st.title("🌍 Travel Trip Planner Chatbot")
st.write("Plan your next adventure with a few simple choices!")

# Step 1: Choose Destination
destinations = df['Destination'].dropna().unique()
destination = st.selectbox("📍 Choose your destination:", sorted(destinations))

# Step 2: Choose Accommodation Type
accommodations = df['Accommodation type'].dropna().unique()
accommodation = st.selectbox("🏨 Choose accommodation type:", sorted(accommodations))

# Step 3: Choose Transportation Type
transportations = df['Transportation type'].dropna().unique()
transport = st.selectbox("🚗 Choose transportation type:", sorted(transportations))

# Button to show itinerary
if st.button("🎒 Show Matching Trips"):
    filtered = df[
        (df['Destination'].str.title() == destination.title()) &
        (df['Accommodation type'].str.title() == accommodation.title()) &
        (df['Transportation type'].str.title() == transport.title())
    ]

    if filtered.empty:
        st.warning("❌ No matching trips found. Try different choices.")
    else:
        st.success(f"✅ Found {len(filtered)} trip(s) matching your preferences!")
        st.dataframe(filtered[['Trip ID', 'Start date', 'End date', 'Duration (days)',
                               'Accommodation cost', 'Transportation cost']])

# Optional: Show top destinations
st.markdown("---")
st.subheader("📊 Top 5 Most Visited Destinations")
top_dest = df['Destination'].value_counts().head(5)
st.bar_chart(top_dest)
