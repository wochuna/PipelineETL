import pandas as pd

# ==========================================
# File Paths
# ==========================================

PROCESSED_DATA_PATH = "data/processed/clean_pipeline_data.csv"


def validate_data():
    """
    Validate the cleaned pipeline sensor data.
    """

    print("=" * 60)
    print("PIPEGUARD AI - DATA QUALITY VALIDATION")
    print("=" * 60)

    df = pd.read_csv(PROCESSED_DATA_PATH)

    print(f"\nValidating {len(df)} records...\n")

    # ==========================================
    # Missing Values
    # ==========================================

    missing_values = df.isnull().sum()

    print("Missing Values:")
    print(missing_values)

    # ==========================================
    # Duplicate Records
    # ==========================================

    duplicate_count = df.duplicated().sum()

    print(f"\nDuplicate Records: {duplicate_count}")

    # ==========================================
    # Flow Validation
    # ==========================================

    invalid_flow = df[
        (df["flow_in"] <= 0) |
        (df["flow_out"] <= 0)
    ]

    print(f"Invalid Flow Records: {len(invalid_flow)}")

    # ==========================================
    # Flow Out should never exceed Flow In
    # ==========================================

    invalid_loss = df[
        df["flow_out"] > df["flow_in"]
    ]

    print(f"Flow Out > Flow In Records: {len(invalid_loss)}")

    # ==========================================
    # Pressure Validation
    # (Only impossible values)
    # ==========================================

    invalid_pressure = df[
        (df["pressure"] < 10) |
        (df["pressure"] > 60)
    ]

    print(f"Invalid Pressure Records: {len(invalid_pressure)}")

    # ==========================================
    # Temperature Validation
    # ==========================================

    invalid_temperature = df[
        (df["temperature"] < 0) |
        (df["temperature"] > 60)
    ]

    print(f"Invalid Temperature Records: {len(invalid_temperature)}")

    # ==========================================
    # Product Loss Validation
    # ==========================================

    negative_loss = df[
        df["loss_litres"] < 0
    ]

    print(f"Negative Loss Records: {len(negative_loss)}")

    # ==========================================
    # Verify Loss Calculation
    # ==========================================

    incorrect_loss = df[
        df["loss_litres"] != (df["flow_in"] - df["flow_out"])
    ]

    print(f"Incorrect Loss Calculations: {len(incorrect_loss)}")

    # ==========================================
    # Operational Anomaly Summary
    # (These DO NOT fail the pipeline)
    # ==========================================

    low_pressure = df[df["pressure"] < 30]

    high_loss = df[df["loss_litres"] > 100]

    alerts = df[df["status"] == "ALERT"]

    print("\n" + "=" * 60)
    print("OPERATIONAL ANOMALY SUMMARY")
    print("=" * 60)

    print(f"Low Pressure Events : {len(low_pressure)}")
    print(f"High Loss Events    : {len(high_loss)}")
    print(f"Alert Records       : {len(alerts)}")

    # ==========================================
    # Final Result
    # ==========================================

    if (
        duplicate_count == 0
        and missing_values.sum() == 0
        and len(invalid_flow) == 0
        and len(invalid_loss) == 0
        and len(invalid_pressure) == 0
        and len(invalid_temperature) == 0
        and len(negative_loss) == 0
        and len(incorrect_loss) == 0
    ):

        print("\nAll data quality checks PASSED.")
        print("=" * 60)

        return True

    else:

        print("\nData quality checks FAILED.")
        print("=" * 60)

        raise ValueError("Data quality validation failed.")


# ==========================================
# Run as standalone script
# ==========================================

if __name__ == "__main__":

    validate_data()