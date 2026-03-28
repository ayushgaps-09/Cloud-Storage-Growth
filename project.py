import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="Cloud Storage Growth Simulator",
    page_icon="☁️",
    layout="wide"
)

st.title("☁️ Cloud Storage Growth Simulator")
st.markdown("### Exponential vs Logistic vs Hybrid Growth Models")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Simulation Controls")

initial_storage = st.sidebar.slider("Initial Storage (GB)", 1, 500, 50)
daily_upload = st.sidebar.slider("Daily Upload (GB/day)", 1, 50, 5)
growth_rate = st.sidebar.slider("Growth Rate", 0.01, 0.2, 0.05)
capacity = st.sidebar.slider("Maximum Capacity (GB)", 100, 5000, 1000)
days_to_simulate = st.sidebar.slider("Simulation Days", 30, 365, 120)
expansion_size = st.sidebar.slider("Expansion Size (GB)", 100, 5000, 500)

# ---------------- MODELS ----------------
def exponential_growth(t, S0, r):
    return S0 * np.exp(r * t)

def logistic_growth(t, K, S0, r):
    A = (K - S0) / S0
    return K / (1 + A * np.exp(-r * t))

def hybrid_model(days, S0, r, K, daily):
    storage = []
    for t in days:
        exp_val = exponential_growth(t, S0, r)
        log_val = logistic_growth(t, K, S0, r)
        value = min(exp_val, log_val) + daily * t
        storage.append(value)
    return np.array(storage)

# ---------------- DATA GENERATION ----------------
days = np.arange(0, days_to_simulate)

exp_storage = exponential_growth(days, initial_storage, growth_rate)
log_storage = logistic_growth(days, capacity, initial_storage, growth_rate)
hybrid_storage = hybrid_model(days, initial_storage, growth_rate, capacity, daily_upload)

df = pd.DataFrame({
    "Day": days,
    "Exponential": exp_storage,
    "Logistic": log_storage,
    "Hybrid": hybrid_storage
})

# ---------------- METRICS ----------------
st.subheader("📊 Current Parameters")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Initial Storage", f"{initial_storage} GB")
col2.metric("Daily Upload", f"{daily_upload} GB/day")
col3.metric("Capacity", f"{capacity} GB")
col4.metric("Growth Rate", f"{growth_rate}")

# ---------------- EXPONENTIAL GRAPH ----------------
st.subheader("📈 Exponential Growth")

fig1, ax1 = plt.subplots()
ax1.plot(days, exp_storage)
ax1.set_xlabel("Days")
ax1.set_ylabel("Storage (GB)")
ax1.set_title("Exponential Growth - Unlimited Increase")
ax1.grid(True)

st.pyplot(fig1)

# ---------------- LOGISTIC GRAPH ----------------
st.subheader("📉 Logistic Growth")

fig2, ax2 = plt.subplots()
ax2.plot(days, log_storage)
ax2.axhline(capacity, linestyle="--")
ax2.set_xlabel("Days")
ax2.set_ylabel("Storage (GB)")
ax2.set_title("Logistic Growth - Saturation Near Capacity")
ax2.grid(True)

st.pyplot(fig2)

# ---------------- HYBRID GRAPH ----------------
st.subheader("☁️ Hybrid Growth Prediction")

fig3, ax3 = plt.subplots()
ax3.plot(days, hybrid_storage, linewidth=2)
ax3.axhline(capacity, linestyle="--")
ax3.set_xlabel("Days")
ax3.set_ylabel("Storage (GB)")
ax3.set_title("Combined Exponential + Logistic Growth")
ax3.grid(True)

st.pyplot(fig3)

# ---------------- CAPACITY ANALYSIS ----------------
st.subheader("🚨 Capacity Analysis")

threshold = 0.8 * capacity
expansion_day = None

for i, val in enumerate(hybrid_storage):
    if val >= threshold:
        expansion_day = i
        break

if expansion_day is not None:
    st.error(f"⚠️ Storage will reach 80% capacity on **day {expansion_day}**.")
    st.info(f"📦 Recommended expansion: **+{expansion_size} GB** before this day.")
else:
    st.success("✅ Storage remains within safe limits.")

# ---------------- EXPANSION SIMULATION ----------------
expanded_capacity = capacity + expansion_size
expanded_storage = np.minimum(hybrid_storage, expanded_capacity)

st.subheader("📉 Storage After Expansion")

fig4, ax4 = plt.subplots()
ax4.plot(days, expanded_storage)
ax4.axhline(expanded_capacity, linestyle="--")
ax4.set_xlabel("Days")
ax4.set_ylabel("Storage (GB)")
ax4.set_title("Storage Growth After Capacity Expansion")
ax4.grid(True)

st.pyplot(fig4)

# ---------------- DATA TABLE ----------------
st.subheader("📋 Daily Storage Data")
st.dataframe(df)

csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download CSV",
    csv,
    "storage_data.csv",
    "text/csv"
)

# ---------------- EXPLANATION ----------------
with st.expander("📘 Model Explanation"):
    st.markdown("""
### Exponential Growth
S(t) = S0 * e^(rt)

Shows rapid, unlimited growth in early stages.

### Logistic Growth
S(t) = K / (1 + A * e^(-rt))

Shows realistic growth that slows as capacity is reached.

### Hybrid Model
This project combines both models and includes daily uploads to simulate real-world cloud storage usage.
""")
