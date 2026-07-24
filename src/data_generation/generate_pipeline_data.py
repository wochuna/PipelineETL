from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
import os

fake = Faker()

# ==========================================
# Configuration
# ==========================================

INITIAL_RECORDS = 10000
LIVE_RECORDS = 10

PIPELINE_SEGMENTS = [
    "A12",
    "A13",
    "B07",
    "B08",
    "C03",
    "D14"
]

STATIONS = [
    "Mombasa Terminal",
    "Nairobi Terminal",
    "Nakuru Depot",
    "Eldoret Depot",
    "Kisumu Depot"
]

OUTPUT_FILE = "data/raw/kpc_pipeline_sensor_data.csv"


# ==========================================
# Generate one sensor record
# ==========================================

def generate_record(timestamp):

    pipeline_segment = random.choice(PIPELINE_SEGMENTS)
    station = random.choice(STATIONS)

    flow_in = random.randint(9500, 10500)
    pressure = round(random.uniform(40, 45), 2)
    temperature = round(random.uniform(24, 32), 2)
    meter_reading = round(random.uniform(500000, 900000), 2)

    anomaly = False
    status = "NORMAL"
    anomaly_type = "No Anomaly"

    if random.random() < 0.05:

        anomaly = True

        anomaly_type = random.choice([
            "Pipeline Leak",
            "Illegal Tapping",
            "Pressure Drop"
        ])

        if anomaly_type == "Pipeline Leak":

            loss = random.randint(150, 500)
            pressure -= random.uniform(5, 10)

        elif anomaly_type == "Illegal Tapping":

            loss = random.randint(200, 700)

        else:

            loss = random.randint(100, 300)
            pressure -= random.uniform(8, 12)

        status = "ALERT"

    else:

        loss = random.randint(0, 30)

    flow_out = flow_in - loss

    return {

        "timestamp": timestamp,
        "pipeline_segment": pipeline_segment,
        "station": station,
        "meter_id": fake.uuid4(),
        "sensor_id": fake.bothify(text="SNS-#####"),
        "flow_in": flow_in,
        "flow_out": flow_out,
        "pressure": round(pressure, 2),
        "temperature": temperature,
        "meter_reading": meter_reading,
        "loss_litres": loss,
        "status": status,
        "anomaly": anomaly,
        "anomaly_type": anomaly_type

    }


# ==========================================
# Initial dataset (10,000 rows)
# ==========================================

def generate_dataset():

    os.makedirs("data/raw", exist_ok=True)

    start_time = datetime.now() - timedelta(days=7)

    records = []

    for i in range(INITIAL_RECORDS):

        timestamp = start_time + timedelta(minutes=5 * i)
        records.append(generate_record(timestamp))

    df = pd.DataFrame(records)

    df.to_csv(OUTPUT_FILE, index=False)

    print("=" * 60)
    print("PIPEGUARD AI INITIAL DATASET GENERATED")
    print("=" * 60)
    print(f"Total Records : {len(df)}")
    print(f"Anomalies     : {df['anomaly'].sum()}")
    print(f"Normal        : {len(df)-df['anomaly'].sum()}")
    print(f"Saved to      : {OUTPUT_FILE}")
    print("=" * 60)

    return df


# ==========================================
# Append new live sensor readings
# ==========================================

def append_live_data(num_records=LIVE_RECORDS):

    if os.path.exists(OUTPUT_FILE):

        existing_df = pd.read_csv(OUTPUT_FILE)

        last_timestamp = pd.to_datetime(
            existing_df["timestamp"].iloc[-1]
        )

    else:

        existing_df = pd.DataFrame()

        last_timestamp = datetime.now()

    records = []

    for i in range(num_records):

        timestamp = last_timestamp + timedelta(minutes=5 * (i + 1))
        records.append(generate_record(timestamp))

    new_df = pd.DataFrame(records)

    if os.path.exists(OUTPUT_FILE):

        new_df.to_csv(
            OUTPUT_FILE,
            mode="a",
            header=False,
            index=False
        )

    else:

        new_df.to_csv(
            OUTPUT_FILE,
            index=False
        )

    print("=" * 60)
    print("NEW SENSOR DATA RECEIVED")
    print("=" * 60)
    print(f"New Records : {len(new_df)}")
    print(f"Alerts      : {new_df['anomaly'].sum()}")
    print(f"Latest Time : {new_df['timestamp'].max()}")
    print("=" * 60)

    return new_df


# ==========================================
# Main
# ==========================================

if __name__ == "__main__":

    if os.path.exists(OUTPUT_FILE):

        append_live_data()

    else:

        generate_dataset()