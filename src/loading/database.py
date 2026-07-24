import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from src.config.settings import DATABASE_URL, PROCESSED_DATA_PATH

# ==========================================
# Database Connection
# ==========================================

engine = create_engine(DATABASE_URL)


def load_to_database():
    """
    Load only new cleaned pipeline sensor data
    into PostgreSQL.
    """

    print("=" * 60)
    print("PIPEGUARD AI - DATA LOADING")
    print("=" * 60)

    try:

        # ==========================================
        # Read processed dataset
        # ==========================================

        df = pd.read_csv(PROCESSED_DATA_PATH)

        df["timestamp"] = pd.to_datetime(df["timestamp"])

        print(f"\nProcessed records available: {len(df)}")

        # ==========================================
        # Check if table exists
        # ==========================================

        try:

            existing_df = pd.read_sql(
                "SELECT timestamp, sensor_id FROM pipeline_sensor_data",
                engine
            )

            existing_df["timestamp"] = pd.to_datetime(
                existing_df["timestamp"]
            )

            print(
                f"Existing database records: {len(existing_df)}"
            )

        except Exception:

            existing_df = pd.DataFrame(
                columns=["timestamp", "sensor_id"]
            )

            print(
                "Database table not found. A new table will be created."
            )

        # ==========================================
        # Keep only records not already in database
        # ==========================================

        if len(existing_df) > 0:

            new_df = df.merge(
                existing_df,
                on=["timestamp", "sensor_id"],
                how="left",
                indicator=True
            )

            new_df = (
                new_df[new_df["_merge"] == "left_only"]
                .drop(columns="_merge")
            )

        else:

            new_df = df

        print(f"New records to load: {len(new_df)}")

        # ==========================================
        # Load only new records
        # ==========================================

        if len(new_df) > 0:

            new_df.to_sql(
                name="pipeline_sensor_data",
                con=engine,
                if_exists="append",
                index=False
            )

            print("\nNew records successfully loaded!")

        else:

            print("\nNo new records to load.")

        # ==========================================
        # Verify final row count
        # ==========================================

        total = pd.read_sql(
            "SELECT COUNT(*) AS total FROM pipeline_sensor_data",
            engine
        )

        print(f"\nTotal records in database: {total['total'][0]}")

        print("Database Table: pipeline_sensor_data")

        print("=" * 60)

        return new_df

    except FileNotFoundError:

        print("Processed dataset not found.")
        raise

    except SQLAlchemyError as e:

        print("Database loading failed.")
        print(e)
        raise

    except Exception as e:

        print("Unexpected error occurred.")
        print(e)
        raise


# ==========================================
# Run as standalone script
# ==========================================

if __name__ == "__main__":

    load_to_database()