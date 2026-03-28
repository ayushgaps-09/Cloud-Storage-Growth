import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Cloud Storage Growth Simulator",
    page_icon="☁️",
    layout="wide"
)

st.title("☁️ Cloud Storage Growth Simulator")
st.markdown("### Predict storage usage using **Exponential + Logistic Growth Model**")

# ------------------ SIDEBAR ------------------
st.sidebar.header("⚙️ Simulation Parameters")

initial_storage = st.sidebar.slider(
    "Initial Storage (GB)", 1, 500, 50
)

daily_upload = st.sidebar.slider(
    "Daily Upload (GB/day)", 1, 50, 5
)

growth_rate = st.sidebar.slider(
    "Growth Rate", 0.01, 0.2, 0.05
)

capacity = st.sidebar.slider(
    "Maximum Storage Capacity (GB)", 100, 5000, 1000
)

days_to_simulate = st.sidebar.slider(
    "Simulation Days", 30, 365, 120
)

expansion_size = st.sidebar.slider(
    "Planned Expansion Size (GB)", 100, 5000, 500
)

# ------------------ MODELS ------------------

def exponential_growth(t, S0, r):
    return S0 * np.exp(r * t)

def logistic_growth(t, K, S0, r):
    A = (K - S0) / S0
    return K / (1 + A * np.exp(-r * t))

# Hybrid model
def hybrid_model(days, S0, r, K, daily):
    storage = []
    for t in days:
        exp_val = exponential_growth(t, S0, r)
        log_val = logistic_growth(t, K, S0, r)

        # switch to logistic when nearing capacity
        value = min(exp_val, log_val) + daily * t
        storage.append(value)
    return np.array(storage)

# ------------------ DATA GENERATION ------------------
days = np.arange(0, days_to_simulate)
storage = hybrid_model(days, initial_storage, growth_rate, capacity, daily_upload)

df = pd.DataFrame({
    "Day": days,
    "Storage Used (GB)": storage
})

# ------------------ METRICS ------------------
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Initial Storage", f"{initial_storage} GB")
col2.metric("Daily Upload", f"{daily_upload} GB")
col3.metric("Capacity", f"{capacity} GB")
col4.metric("Growth Rate", f"{growth_rate}")

# ------------------ GRAPH ------------------
st.subheader("📈 Storage Growth Forecast")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(days, storage, label="Predicted Storage", linewidth=2)
ax.axhline(capacity, linestyle="--", label="Max Capacity")
ax.set_xlabel("Days")
ax.set_ylabel("Storage (GB)")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# ------------------ CAPACITY ANALYSIS ------------------
st.subheader("🚨 Capacity & Expansion Planning")

threshold = 0.8 * capacity
expansion_day = None

for i, val in enumerate(storage):
    if val >= threshold:
        expansion_day = i
        break

if expansion_day:
    st.error(
        f"⚠️ Storage will reach **80% capacity on day {expansion_day}**."
    )
    st.info(
        f"📦 Recommended: Expand storage by **{expansion_size} GB** before day {expansion_day}"
    )
else:
    st.success("✅ Storage remains within safe limits during simulation.")

# ------------------ EXPANSION SIMULATION ------------------
expanded_capacity = capacity + expansion_size

expanded_storage = np.minimum(storage, expanded_capacity)

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(days, expanded_storage, label="After Expansion")
ax2.axhline(expanded_capacity, linestyle="--", label="Expanded Capacity")
ax2.legend()
ax2.grid(True)

st.subheader("📉 After Expansion Scenario")
st.pyplot(fig2)

# ------------------ DATA TABLE ------------------
st.subheader("📋 Daily Storage Data")
st.dataframe(df)

# download option
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download Data as CSV",
    csv,
    "storage_simulation.csv",
    "text/csv"
)

# ------------------ MODEL EXPLANATION ------------------
with st.expander("📘 Model Explanation"):
    st.markdown("""
### Exponential Growth
Early-stage cloud usage grows rapidly:
S(t) = S0 * e^(rt)

### Logistic Growth
As storage approaches capacity:
S(t) = K / (1 + A e^(-rt))

### Hybrid Model
This project combines both models to simulate real-world storage usage.
""")
