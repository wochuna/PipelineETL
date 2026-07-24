import time

from src.data_generation.generate_pipeline_data import generate_dataset
from src.ingestion.extract import extract_data
from src.transformation.clean import clean_data
from src.validation.quality_checks import validate_data
from src.loading.database import load_to_database


def run_pipeline():
    """
    Execute the complete ETL pipeline.
    """

    start_time = time.time()

    print("=" * 70)
    print("           PIPEGUARD AI - ETL PIPELINE")
    print("=" * 70)

    try:
        # ==========================================
        # Step 1 - Generate Synthetic Data
        # ==========================================

        print("\n[1/5] Generating synthetic pipeline sensor data...")
        generate_dataset()

        # ==========================================
        # Step 2 - Extract Data
        # ==========================================

        print("\n[2/5] Extracting raw dataset...")
        extract_data()

        # ==========================================
        # Step 3 - Clean Data
        # ==========================================

        print("\n[3/5] Cleaning and transforming dataset...")
        clean_data()

        # ==========================================
        # Step 4 - Validate Data
        # ==========================================

        print("\n[4/5] Running data quality validation...")
        validate_data()

        # ==========================================
        # Step 5 - Load Data
        # ==========================================

        print("\n[5/5] Loading data into PostgreSQL...")
        load_to_database()

        execution_time = round(time.time() - start_time, 2)

        print("\n" + "=" * 70)
        print("ETL PIPELINE COMPLETED SUCCESSFULLY")
        print(f"Execution Time: {execution_time} seconds")
        print("=" * 70)

    except Exception as e:

        print("\n" + "=" * 70)
        print("ETL PIPELINE FAILED")
        print("=" * 70)
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    run_pipeline()