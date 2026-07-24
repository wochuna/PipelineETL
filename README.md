
# PipeGuard AI - Stage 1: Data Engineering Foundation

## Overview

PipeGuard AI is a data engineering project developed by AVENGERS GROUP for the Inuka Hackathon 2026.

This stage focuses on building a reliable and automated ETL (Extract, Transform, Load) pipeline for pipeline operational data. The objective is to ingest messy sensor data, clean and validate it, and store it in a structured database that can serve as a trusted foundation for future analytics.

---

## Problem Statement

Domain A: Pipeline Integrity & Product Loss

Problem 1: Shrinkage Detection

Detect and quantify product losses and anomalies along a petroleum pipeline network using operational data such as flow meter readings, pressure, and temperature.

Operational pipeline data is often incomplete, inconsistent, or noisy. Without a reliable data pipeline, it is difficult to identify potential losses or support informed operational decisions.

---

## Stage Objective

Build a production-ready data pipeline that:

- Ingests raw pipeline sensor data
- Cleans and transforms operational records
- Validates data quality using predefined business rules
- Calculates product loss values
- Loads clean data into PostgreSQL
- Provides automated testing and Continuous Integration (CI)

---

## Project Features

- Synthetic KPC-like pipeline telemetry generation
- Automated ETL pipeline
- Data cleaning and preprocessing
- Data quality validation
- Product loss calculation
- PostgreSQL data storage
- GitHub Actions Continuous Integration


## Project Structure

```text
PipeGuard-AI/
├── dashboard/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── database/
│
├── src/
│   ├── data_generation/
│   ├── analytics/
│   ├── config/
│   ├── ingestion/
│   ├── transformation/
│   ├── validation/
│   ├── loading/
│   └── main.py
│
├── tests/
│
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```


## ETL Workflow

```
Raw Pipeline Data
        │
        ▼
Extract Data
        │
        ▼
Clean & Transform
        │
        ▼
Validate Data Quality
        │
        ▼
Calculate Product Loss
        │
        ▼
Load into PostgreSQL
```


## Technology Stack

| Component        | Technology     |
| ---------------- | -------------- |
| Language         | Python 3       |
| Data Processing  | Pandas         |
| Synthetic Data   | Faker          |
| Database         | PostgreSQL     |
| ORM              | SQLAlchemy     |
| Visualization    | Streamlit      |
| CI               | GitHub Actions |


## Getting Started

### Clone the repository

```bash
git clone https://github.com/wochuna/pipeguard-ai.git
cd PipeGuard-AI
```

### Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment.

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```
## 5. Install Additional Packages

If these packages are not already included in `requirements.txt`, install them manually.

### Faker

```bash
pip install faker
```

### Streamlit

```bash
pip install streamlit
```
## 6. Configure Environment Variables

Create a `.env` file in the project root and add your PostgreSQL credentials.

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=pipeguard_ai

RAW_DATA_PATH=data/raw/kpc_pipeline_sensor_data.csv
PROCESSED_DATA_PATH=data/processed/clean_pipeline_data.csv
```
## 7. Run the ETL Pipeline

Run the complete ETL workflow:

```bash
python -m src.main
```

The pipeline will:

- Generate synthetic pipeline sensor data
- Extract the raw dataset
- Clean and transform the data
- Validate data quality
- Calculate product loss
- Load the processed data into PostgreSQL

---

## 8. Launch the Dashboard

Start the Streamlit dashboard:

```bash
streamlit run dashboard/app.py
```

After the server starts, open your browser and visit:

```
http://localhost:8501
```

The dashboard provides:

- Pipeline Health Score
- Flow In vs Flow Out Monitoring
- Product Loss Trends
- Operational Anomaly Detection
- Pipeline Segment Performance
- Highest Product Loss Events
- Interactive Filters


## Team

AVENGERS GROUP

- Clement Mwangi
- Elly Arwa
- Michael Randa
- Macharia Kariuki
- Yvonne Wochuna


## License

This project is developed for educational and hackathon purposes.
