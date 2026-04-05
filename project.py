import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Cloud Storage Growth Model", page_icon="☁️", layout="wide")

st.title("☁️ CLOUD STORAGE GROWTH MODEL")
st.markdown("### Exponential vs Logistic vs Hybrid Growth Models")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Simulation Control")

# Input mode (Slider + Manual)
input_mode = st.sidebar.radio("Choose Input Method", ["Slider", "Manual Input"])

if input_mode == "Slider":
    initial_storage = st.sidebar.slider("Initial Storage (GB)", 1, 500, 10)
    daily_upload = st.sidebar.slider("Daily Upload (GB/day)", 1, 50, 1)
    growth_rate = st.sidebar.slider("Growth Rate", 0.01, 0.2, 0.02)
    capacity = st.sidebar.slider("Maximum Capacity (GB)", 100, 5000, 3818)
    days_to_simulate = st.sidebar.slider("Simulation Days", 30, 365, 30)
    expansion_size = st.sidebar.slider("Expansion Size (GB)", 100, 5000, 100)
else:
    initial_storage = st.sidebar.number_input("Initial Storage (GB)", value=10)
    daily_upload = st.sidebar.number_input("Daily Upload (GB/day)", value=1)
    growth_rate = st.sidebar.number_input("Growth Rate", value=0.02)
    capacity = st.sidebar.number_input("Maximum Capacity (GB)", value=3818)
    days_to_simulate = st.sidebar.number_input("Simulation Days", value=30)
    expansion_size = st.sidebar.number_input("Expansion Size (GB)", value=100)

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
days = np.arange(0, int(days_to_simulate))

exp_storage = exponential_growth(days, initial_storage, growth_rate)
log_storage = logistic_growth(days, capacity, initial_storage, growth_rate)
hybrid_storage = hybrid_model(days, initial_storage, growth_rate, capacity, daily_upload)

# ---------------- EXPONENTIAL GRAPH ----------------
st.subheader("📈 Exponential Growth")

fig1, ax1 = plt.subplots()
ax1.plot(days, exp_storage, label="Exponential Growth", linewidth=2)
ax1.set_xlabel("Days")
ax1.set_ylabel("Storage (GB)")
ax1.set_title("Exponential Growth")
ax1.grid(True)
ax1.legend(loc="upper left")
st.pyplot(fig1)

# ---------------- LOGISTIC GRAPH ----------------
st.subheader("📉 Logistic Growth")

fig2, ax2 = plt.subplots()
ax2.plot(days, log_storage, label="Logistic Growth", linewidth=2)
ax2.axhline(capacity, linestyle="--", label="Capacity Limit")
ax2.set_xlabel("Days")
ax2.set_ylabel("Storage (GB)")
ax2.set_title("Logistic Growth")
ax2.grid(True)
ax2.legend(loc="upper left")
st.pyplot(fig2)

# ---------------- HYBRID GRAPH ----------------
st.subheader("☁️ Hybrid Growth")

fig3, ax3 = plt.subplots()
ax3.plot(days, hybrid_storage, label="Hybrid Model", linewidth=2)
ax3.axhline(capacity, linestyle="--", label="Capacity Limit")
ax3.set_xlabel("Days")
ax3.set_ylabel("Storage (GB)")
ax3.set_title("Hybrid Growth")
ax3.grid(True)
ax3.legend(loc="upper left")
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
    st.markdown(f"""
    <div style="background-color:#4b1e1e;padding:20px;border-radius:15px;margin-bottom:15px">
        <h3 style="color:#ff6b6b;">⚠️ Storage will reach 80% capacity on day {expansion_day}</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background-color:#1e3a5f;padding:20px;border-radius:15px;">
        <h3 style="color:#4dabf7;">📦 Recommended expansion: +{expansion_size} GB before this day</h3>
    </div>
    """, unsafe_allow_html=True)

else:
    st.success("✅ Storage remains within safe limits.")

# ---------------- EXPANSION GRAPH ----------------
expanded_capacity = capacity + expansion_size
expanded_storage = np.minimum(hybrid_storage, expanded_capacity)

st.subheader("📉 Storage After Expansion")

fig4, ax4 = plt.subplots()
ax4.plot(days, expanded_storage, label="After Expansion", linewidth=2)
ax4.axhline(expanded_capacity, linestyle="--", label="New Capacity")
ax4.set_xlabel("Days")
ax4.set_ylabel("Storage (GB)")
ax4.set_title("Storage After Expansion")
ax4.grid(True)
ax4.legend(loc="upper left")
st.pyplot(fig4)

# ---------------- DATA TABLE ----------------
st.subheader("📋 DAILY STORAGE DATA")

df = pd.DataFrame({
    "Day": days,
    "Exponential": exp_storage,
    "Logistic": log_storage,
    "Hybrid": hybrid_storage
})

st.dataframe(df, use_container_width=True)

# Download button
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
➡️ Fast and unlimited growth

### Logistic Growth
S(t) = K / (1 + A * e^(-rt))  
➡️ Growth slows near capacity

### Hybrid Model
➡️ Combines real-world usage with daily uploads
➡️ Most realistic model
""")
