from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
import pandas as pd
import threading
import time

# ==== PubNub Setup ====
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-99084bc5-1844-4e1c-82ca-a01b18166ca8"
pnconfig.uuid = "cowabunga-sensor-pull"
pubnub = PubNub(pnconfig)

# ==== Data Capture ====
sensor_data = []
DATA_LIMIT = 100  # Adjust if you want more or less

# ==== Threading event to allow clean exit ====
data_collected = threading.Event()

# ==== Flexible Listener ====
class SensorDataListener(SubscribeCallback):
    def message(self, pubnub, message):
        payload = message.message
        
        print("\n📡 Raw message received:")
        print(payload)  # <- This shows you exactly what the keys are

        # Save only if it's a dictionary (JSON-style object)
        if isinstance(payload, dict):
            sensor_data.append(payload)

        if len(sensor_data) >= DATA_LIMIT:
            pubnub.unsubscribe_all()
            data_collected.set()

# ==== Start Subscription ====
pubnub.add_listener(SensorDataListener())
pubnub.subscribe().channels("pubnub-sensor-network").execute()

# ==== Wait for Data ====
print(f"⏳ Collecting {DATA_LIMIT} messages from 'pubnub-sensor-network'...")
data_collected.wait()

# ==== Convert to DataFrame ====
df = pd.DataFrame(sensor_data)
print("\n✅ DataFrame created. Preview:")
print(df.head())

# ==== Save to CSV ====
csv_file = "cowabunga_sensor_data.csv"
df.to_csv(csv_file, index=False)
print(f"\n💾 Saved sensor data to '{csv_file}'")
