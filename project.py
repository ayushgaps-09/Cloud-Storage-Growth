import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cloud Storage Growth Model", layout="wide")

st.title("☁️ Cloud Storage Growth Predictor")
st.write("This app predicts corporate cloud storage usage using a logistic growth model.")

# Sidebar Inputs
st.sidebar.header("Model Parameters")

initial_storage = st.sidebar.slider(
    "Initial Storage Used (GB)", min_value=1, max_value=500, value=50
)

growth_rate = st.sidebar.slider(
    "Growth Rate", min_value=0.01, max_value=0.2, value=0.05, step=0.01
)

capacity = st.sidebar.slider(
    "Maximum Storage Capacity (GB)", min_value=100, max_value=5000, value=1000
)

days_to_simulate = st.sidebar.slider(
    "Days to Simulate", min_value=30, max_value=365, value=120
)

# Logistic Growth Function
def storage_growth(t, K, S0, r):
    A = (K - S0) / S0
    return K / (1 + A * np.exp(-r * t))

# Generate Data
days = np.linspace(0, days_to_simulate, days_to_simulate)
storage = storage_growth(days, capacity, initial_storage, growth_rate)

# Plot Graph
st.subheader("📈 Storage Growth Over Time")

fig, ax = plt.subplots()
ax.plot(days, storage)
ax.axhline(capacity, linestyle="--")
ax.set_xlabel("Days")
ax.set_ylabel("Storage Used (GB)")
ax.set_title("Predicted Cloud Storage Usage")

st.pyplot(fig)

# Capacity Analysis
st.subheader("📊 Capacity Analysis")

current_day_80 = None
for i, val in enumerate(storage):
    if val >= 0.8 * capacity:
        current_day_80 = i
        break

col1, col2, col3 = st.columns(3)

col1.metric("Initial Storage", f"{initial_storage} GB")
col2.metric("Capacity", f"{capacity} GB")
col3.metric("Growth Rate", f"{growth_rate}")

if current_day_80:
    st.warning(f"⚠️ Storage will reach **80% capacity** around **day {current_day_80}**. Plan expansion before this.")
else:
    st.success("Storage will remain below 80% capacity within the simulation period.")

# Data Table
st.subheader("📋 Simulated Data")

data = {
    "Day": days.astype(int),
    "Storage Used (GB)": storage.round(2)
}

st.dataframe(data)

# Project Explanation Section
with st.expander("📘 Model Explanation"):
    st.write("""
    The model uses **logistic growth** to simulate cloud storage usage:

    S(t) = K / (1 + A * e^(-rt))

    where:
    - S(t): storage at time t
    - K: storage capacity
    - r: growth rate
    - A: constant from initial storage
    """)