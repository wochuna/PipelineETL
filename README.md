
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
- Docker support
- GitHub Actions Continuous Integration
- Unit testing with Pytest

---

## Project Structure

```text
PipeGuard-AI/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── database/
│
├── src/
│   ├── data_generation/
│   ├── ingestion/
│   ├── transformation/
│   ├── validation/
│   ├── loading/
│   └── main.py
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ETL Workflow

```text
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

---

## Technology Stack

| Component        | Technology     |
| ---------------- | -------------- |
| Language         | Python 3       |
| Data Processing  | Pandas         |
| Synthetic Data   | Faker          |
| Database         | PostgreSQL     |
| ORM              | SQLAlchemy     |
| Validation       | Pandera        |
| Testing          | Pytest         |
| Containerization | Docker         |
| CI               | GitHub Actions |

---

## Getting Started

### Clone the repository

```bash
git clone https://github.com/E-Macharia/pipeguard-ai.git
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

### Install Faker

```bash
pip install faker pandas numpy
```

### Start PostgreSQL

```bash
docker compose up -d
```

### Generate synthetic data

```bash
python src/data_generation/generate_pipeline_data.py
```

### Run the ETL pipeline

```bash
python src/main.py
```

### Run tests

```bash
pytest
```

---

## Expected Outputs

Running the pipeline will generate:

- Cleaned pipeline dataset
- Data quality validation report
- Product loss calculations
- PostgreSQL database records

---

## Team

AVENGERS GROUP

- Clement Mwangi
- Elly Arwa
- Michael Randa
- Macharia Kariuki
- Yvonne Wochuna

---

## License

This project is developed for educational and hackathon purposes.
