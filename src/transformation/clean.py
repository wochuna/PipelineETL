import os
import pandas as pd

# ==========================================
# File Paths
# ==========================================

RAW_DATA_PATH = "data/raw/kpc_pipeline_sensor_data.csv"
PROCESSED_DATA_PATH = "data/processed/clean_pipeline_data.csv"


def clean_data():
    """
    Clean newly generated pipeline sensor data and append
    only new records to the processed dataset.
    """

    print("=" * 60)
    print("PIPEGUARD AI - DATA CLEANING")
    print("=" * 60)

    # ------------------------------------------
    # Read raw dataset
    # ------------------------------------------

    raw_df = pd.read_csv(RAW_DATA_PATH)

    print(f"\nRaw dataset records: {len(raw_df)}")

    # ------------------------------------------
    # Missing values
    # ------------------------------------------

    print("\nChecking missing values...")

    print(raw_df.isnull().sum())

    # ------------------------------------------
    # Remove duplicates
    # ------------------------------------------

    duplicate_count = raw_df.duplicated().sum()

    print(f"\nDuplicate records found: {duplicate_count}")

    raw_df = raw_df.drop_duplicates()

    # ------------------------------------------
    # Remove missing critical values
    # ------------------------------------------

    critical_columns = [
        "timestamp",
        "flow_in",
        "flow_out",
        "pressure",
        "temperature"
    ]

    before = len(raw_df)

    raw_df = raw_df.dropna(subset=critical_columns)

    print(
        f"Rows removed because of missing values: {before-len(raw_df)}"
    )

    # ------------------------------------------
    # Standardize data
    # ------------------------------------------

    raw_df["timestamp"] = pd.to_datetime(raw_df["timestamp"])

    raw_df["pipeline_segment"] = (
        raw_df["pipeline_segment"]
        .str.upper()
    )

    raw_df["station"] = (
        raw_df["station"]
        .str.title()
    )

    raw_df["status"] = (
        raw_df["status"]
        .str.upper()
    )

    raw_df["loss_litres"] = (
        raw_df["flow_in"] -
        raw_df["flow_out"]
    )

    raw_df = raw_df.sort_values("timestamp")

    # ------------------------------------------
    # Only keep NEW records
    # ------------------------------------------

    if os.path.exists(PROCESSED_DATA_PATH):

        processed_df = pd.read_csv(PROCESSED_DATA_PATH)

        processed_df["timestamp"] = pd.to_datetime(
            processed_df["timestamp"]
        )

        latest_processed = processed_df["timestamp"].max()

        new_records = raw_df[
            raw_df["timestamp"] > latest_processed
        ]

        print(
            f"\nPreviously processed records: {len(processed_df)}"
        )

    else:

        processed_df = pd.DataFrame()

        new_records = raw_df

        print("\nNo processed dataset found.")

    print(f"New records detected: {len(new_records)}")

    # ------------------------------------------
    # Save processed dataset
    # ------------------------------------------

    os.makedirs("data/processed", exist_ok=True)

    if len(new_records) > 0:

        if os.path.exists(PROCESSED_DATA_PATH):

            new_records.to_csv(
                PROCESSED_DATA_PATH,
                mode="a",
                header=False,
                index=False
            )

        else:

            new_records.to_csv(
                PROCESSED_DATA_PATH,
                index=False
            )

        print(f"Appended {len(new_records)} new records.")

    else:

        print("No new records to process.")

    print("\nCleaning completed successfully!")

    print("=" * 60)

    return new_records


# ==========================================
# Run
# ==========================================

if __name__ == "__main__":

    cleaned_df = clean_data()

    print("\nFirst five new records:\n")

    print(cleaned_df.head())