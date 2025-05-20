import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Tactical dark theme
st.set_page_config(page_title="Cowabunga Command Center", layout="wide")

st.markdown("""
<style>
body {
    background-color: #0F1117;
    color: #E0E0E0;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
# 🛰️ Cowabunga Command Center
*Survival-ready environmental intelligence system.*  
**Powered by pizza. Built for bunkers.**
""")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("sensor_anomalies.csv", parse_dates=["timestamp"])

df = load_data()

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filters")
    cluster_select = st.multiselect("Show Clusters", options=df['cluster'].unique(), default=df['cluster'].unique())
    show_anomalies = st.checkbox("Show only anomalies", value=False)

filtered = df[df['cluster'].isin(cluster_select)]
if show_anomalies:
    filtered = filtered[filtered['is_anomaly'] == 1]

# Summary Boxes
st.markdown("### 🧠 Current Environmental Summary")
col1, col2 = st.columns(2)
col1.metric("☢️ Critical Radiation", int((df['radiation_alert'] == "☢️ CRITICAL").sum()))
col1.metric("⚠️ Elevated Radiation", int((df['radiation_alert'] == "⚠️ Elevated").sum()))
col2.metric("💧 Too Humid", int((df['humidity_alert'] == "💧 Too Humid").sum()))
col2.metric("🌵 Too Dry", int((df['humidity_alert'] == "🌵 Too Dry").sum()))

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Cluster Map",
    "🚨 Anomaly Watch",
    "☢️ Radiation Alerts",
    "📈 Sensor Trends"
])

# === TAB 1: CLUSTER MAP ===
with tab1:
    st.subheader("Sensor Clusters by Environment")
    fig1, ax1 = plt.subplots()
    scatter = ax1.scatter(
        filtered['photosensor'],
        filtered['ambient_temperature'],
        c=filtered['cluster'],
        cmap='viridis',
        alpha=0.7
    )
    ax1.set_xlabel("Photosensor (w/m²)")
    ax1.set_ylabel("Ambient Temp (°C)")
    ax1.set_title("Clustered Sensor Environments")
    st.pyplot(fig1)

# === TAB 2: ANOMALY WATCH ===
with tab2:
    st.subheader("⚠️ Anomaly Detection")
    anomalies = df[df['is_anomaly'] == 1]
    st.metric("Detected Anomalies", len(anomalies))
    if not anomalies.empty:
        st.dataframe(anomalies[['sensor_uuid', 'radiation_level', 'ambient_temperature', 'humidity', 'timestamp']])
        st.warning("Check these sensors for potential system failures or environmental hazards.")
    else:
        st.success("No anomalies detected at this time.")

# === TAB 3: CRITICAL RADIATION ===
with tab3:
    st.subheader("☢️ Critical Radiation Zones")
    critical_df = df[df['radiation_alert'] == "☢️ CRITICAL"]
    if not critical_df.empty:
        st.error("🚨 CRITICAL RADIATION DETECTED")
        st.dataframe(critical_df[['sensor_uuid', 'radiation_level', 'ambient_temperature', 'timestamp']])
    else:
        st.success("All radiation levels are within acceptable bounds.")

# === TAB 4: SENSOR TRENDS ===
with tab4:
    st.subheader("📈 Sensor Metric Trends")
    selected_metric = st.selectbox("Select Metric", ['ambient_temperature', 'humidity', 'photosensor', 'radiation_level'])
    fig2, ax2 = plt.subplots()
    sns.lineplot(data=df, x='timestamp', y=selected_metric, ax=ax2)
    ax2.set_title(f"{selected_metric.replace('_', ' ').title()} Over Time")
    ax2.set_ylabel(selected_metric.replace("_", " ").title())
    ax2.set_xlabel("Timestamp")
    st.pyplot(fig2)
