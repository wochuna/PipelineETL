from dotenv import load_dotenv
import os


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is missing.")

RAW_DATA_PATH = os.getenv(
    "RAW_DATA_PATH",
    "data/raw/kpc_pipeline_sensor_data.csv"
)

PROCESSED_DATA_PATH = os.getenv(
    "PROCESSED_DATA_PATH",
    "data/processed/clean_pipeline_data.csv"
)