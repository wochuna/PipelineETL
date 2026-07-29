from pathlib import Path
from dotenv import load_dotenv
import os

# ---------------------------------------------------------
# Load environment variables from the project root .env file
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

# ---------------------------------------------------------
# Database configuration
# ---------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is missing. "
        "Create a .env file in the project root and add:\\n"
        "DATABASE_URL=postgresql://username:password@host/database?sslmode=require"
    )

# ---------------------------------------------------------
# Data paths
# ---------------------------------------------------------
RAW_DATA_PATH = os.getenv(
    "RAW_DATA_PATH",
    str(BASE_DIR / "data" / "raw" / "kpc_pipeline_sensor_data.csv")
)

PROCESSED_DATA_PATH = os.getenv(
    "PROCESSED_DATA_PATH",
    str(BASE_DIR / "data" / "processed" / "clean_pipeline_data.csv")
)

# ---------------------------------------------------------
# Streamlit / app configuration
# ---------------------------------------------------------
APP_NAME = os.getenv("APP_NAME", "PipeGuard AI")
CACHE_TTL = int(os.getenv("CACHE_TTL", "5"))