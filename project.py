import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="Cloud Storage Growth Model",
    page_icon="☁️",
    layout="wide"
)

st.title(" CLOUD STORAGE GROWTH MODEL")
st.markdown("### Exponential vs Logistic vs Hybrid Growth Models")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Simulation Control")

initial_storage = st.sidebar.slider("Initial Storage (GB)", 1, 500, 10)
daily_upload = st.sidebar.slider("Daily Upload (GB/day)", 1, 50, 1)
growth_rate = st.sidebar.slider("Growth Rate", 0.01, 0.2, 0.02)
capacity = st.sidebar.slider("Maximum Capacity (GB)", 100, 5000, 3818)
days_to_simulate = st.sidebar.slider("Simulation Days", 30, 365, 30)
expansion_size = st.sidebar.slider("Expansion Size (GB)", 100, 5000, 100)

# ---------------- SHOW INPUT VALUES ----------------
st.subheader("📌 Selected Input Values")
st.write(f"Initial Storage: {initial_storage} GB")
st.write(f"Daily Upload: {daily_upload} GB/day")
st.write(f"Growth Rate: {growth_rate}")
st.write(f"Capacity: {capacity} GB")
st.write(f"Simulation Days: {days_to_simulate}")
st.write(f"Expansion Size: {expansion_size} GB")

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

# ---------------- DATA ----------------
days = np.arange(0, days_to_simulate)

exp_storage = exponential_growth(days, initial_storage, growth_rate)
log_storage = logistic_growth(days, capacity, initial_storage, growth_rate)
hybrid_storage = hybrid_model(days, initial_storage, growth_rate, capacity, daily_upload)

# ---------------- EXPONENTIAL GRAPH ----------------
st.subheader("📈 Exponential Growth")

fig1, ax1 = plt.subplots()
ax1.plot(days, exp_storage, label="Exponential Growth")
ax1.set_xlabel("Days")
ax1.set_ylabel("Storage (GB)")
ax1.set_title("Exponential Growth")
ax1.legend()
ax1.grid(True)
st.pyplot(fig1)

# ---------------- LOGISTIC GRAPH ----------------
st.subheader("📉 Logistic Growth")

fig2, ax2 = plt.subplots()
ax2.plot(days, log_storage, label="Logistic Growth")
ax2.axhline(capacity, linestyle="--", label="Max Capacity")
ax2.set_xlabel("Days")
ax2.set_ylabel("Storage (GB)")
ax2.set_title("Logistic Growth")
ax2.legend()
ax2.grid(True)
st.pyplot(fig2)

# ---------------- HYBRID GRAPH ----------------
st.subheader("☁️ Hybrid Growth")

fig3, ax3 = plt.subplots()
ax3.plot(days, hybrid_storage, linewidth=2, label="Hybrid Model")
ax3.axhline(capacity, linestyle="--", label="Capacity Limit")
ax3.set_xlabel("Days")
ax3.set_ylabel("Storage (GB)")
ax3.set_title("Hybrid Growth")
ax3.legend()
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
    st.error(f"⚠️ Storage reaches 80% on day {expansion_day}")
    st.info(f"📦 Add +{expansion_size} GB before this day")
else:
    st.success("✅ Storage is safe")

# ---------------- EXPANSION GRAPH ----------------
expanded_capacity = capacity + expansion_size
expanded_storage = np.minimum(hybrid_storage, expanded_capacity)

st.subheader("📉 After Expansion")

fig4, ax4 = plt.subplots()
ax4.plot(days, expanded_storage, label="After Expansion")
ax4.axhline(expanded_capacity, linestyle="--", label="New Capacity")
ax4.set_xlabel("Days")
ax4.set_ylabel("Storage (GB)")
ax4.set_title("Storage After Expansion")
ax4.legend()
ax4.grid(True)
st.pyplot(fig4)

# ---------------- EXPLANATION ----------------
st.subheader("📘 Explanation (Dynamic)")

if growth_rate > 0.1:
    st.write("🔴 High growth rate → Storage increases very fast")
else:
    st.write("🟢 Low growth rate → Storage increases slowly")

if daily_upload > 20:
    st.write("🔴 High daily upload → Faster capacity usage")
else:
    st.write("🟢 Low daily upload → Slower usage")

if capacity < 1000:
    st.write("⚠️ Low capacity → System will fill quickly")
else:
    st.write("✅ High capacity → More storage available")

# ---------------- DATA TABLE ----------------
df = pd.DataFrame({
    "Day": days,
    "Exponential": exp_storage,
    "Logistic": log_storage,
    "Hybrid": hybrid_storage
})

st.subheader("📋 Data Table")
st.dataframe(df)
