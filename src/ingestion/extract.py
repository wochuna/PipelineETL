import os
import pandas as pd

# ==========================================
# File Paths
# ==========================================

RAW_DATA_PATH = "data/raw/kpc_pipeline_sensor_data.csv"


def extract_data():
    """
    Extract raw pipeline sensor data from CSV.
    """

    print("=" * 60)
    print("PIPEGUARD AI - DATA EXTRACTION")
    print("=" * 60)

    # ==========================================
    # Check if file exists
    # ==========================================

    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(
            f"Dataset not found: {RAW_DATA_PATH}"
        )

    # ==========================================
    # Read CSV
    # ==========================================

    df = pd.read_csv(RAW_DATA_PATH)

    # ==========================================
    # Display extraction summary
    # ==========================================

    print(f"\nSuccessfully extracted {len(df)} records.")

    print(f"Number of columns: {len(df.columns)}")

    print("\nColumns:")

    for column in df.columns:
        print(f"• {column}")

    print("\nExtraction completed successfully.")

    print("=" * 60)

    return df


# ==========================================
# Run as standalone script
# ==========================================

if __name__ == "__main__":

    extracted_df = extract_data()

    print("\nFirst 5 records:\n")

    print(extracted_df.head())