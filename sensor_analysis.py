import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

# Load sensor data
df = pd.read_csv("cowabunga_sensor_data.csv")
df.columns = df.columns.str.lower()
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Select features for ML
features = ['ambient_temperature', 'humidity', 'photosensor', 'radiation_level']
X = df[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# === KMeans Clustering ===
kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(X_scaled)

# === Isolation Forest Anomaly Detection ===
isoforest = IsolationForest(contamination=0.05, random_state=42)
isoforest.fit(X_scaled)
df['anomaly_score'] = isoforest.decision_function(X_scaled)
df['is_anomaly'] = isoforest.predict(X_scaled).astype(int)
df['is_anomaly'] = df['is_anomaly'].apply(lambda x: 1 if x == -1 else 0)

# === Alert Flags ===
def radiation_status(r):
    if r > 200:
        return "☢️ CRITICAL"
    elif r > 175:
        return "⚠️ Elevated"
    else:
        return "✅ Normal"

def humidity_status(h):
    if h > 85:
        return "💧 Too Humid"
    elif h < 30:
        return "🌵 Too Dry"
    else:
        return "👌 Optimal"

df['radiation_alert'] = df['radiation_level'].apply(radiation_status)
df['humidity_alert'] = df['humidity'].apply(humidity_status)

# Save enhanced dataset
df.to_csv("sensor_anomalies.csv", index=False)
print("✅ Sensor analysis complete. Saved to 'sensor_anomalies.csv'.")
