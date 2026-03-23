# Health-Tech Logistics: Supply Chain Analytics Pipeline

## Overview
This project builds an end-to-end ETL pipeline for health commodity shipment data, transforming raw Airtable records into an interactive analytics dashboard that tells a story about **delivery efficiency** and **cost optimization** across global health supply chains.

---

## Architecture

```
Kaggle Dataset (USAID)
       ↓
  Airtable Base (Raw Storage)
       ↓
  Python ETL Scripts (Extraction + Transformation)
       ↓
  DuckDB (Local Data Store)
       ↓
  Supabase PostgreSQL (Cloud Database)
       ↓
  Preset.io / Apache Superset (Dashboard)
```

---

## Dashboard
🔗 **Live Dashboard:** [Health Commodities Logistics Intelligence](https://f60043fb.us1a.app.preset.io/superset/dashboard/8/?native_filters_key=ZZRyZzJ6Ttc)

### Dashboard Story
The dashboard answers three critical questions for logistics directors:

1. **Supply Chain Health:** Ethiopia and Namibia have the highest average freight costs (~$22k and ~$20k respectively), signaling a need for vendor renegotiation or route optimization in these regions.

2. **Operational Efficiency:** On-Time Delivery trends show significant fluctuation between 2006–2009, with peaks suggesting seasonal or regional bottlenecks that need targeted intervention.

3. **Cost Strategy:** Air shipments have an average Cost per KG of ~$45 — far higher than other modes — confirming that over-reliance on Air freight for heavy loads is a major cost driver.

---

## Data Quality Issues Found (EDA)

| # | Issue | Details |
|---|-------|---------|
| 1 | **Missing Values** | Multiple columns had missing data, particularly `Delivered to Client Date` and `Freight Cost (USD)` |
| 2 | **Outliers** | Extreme values in `Freight Cost (USD)` and `Weight (Kilograms)` detected via IQR method |
| 3 | **Inconsistent Naming** | `Shipment Mode` had casing/whitespace inconsistencies (e.g. "air", "AIR", "Air") |
| 4 | **Zero/Negative Values** | Some records had zero or negative weights and freight costs |

---

## Hypothesis: Air vs. Truck Cost-Effectiveness

> **Air shipments have a significantly higher Cost per KG than Truck shipments for loads exceeding 500 kg.** While Air freight ensures faster and more reliable on-time delivery, the cost premium makes it economically inefficient for heavy commodities. Truck shipments, despite higher late delivery rates, offer a more cost-effective solution for bulk health commodities where delivery urgency is low. This suggests the organization should reserve Air shipments for urgent, lightweight orders and default to Truck/Road for heavy, non-urgent commodities.

---

## Repository Structure

```
health-tech-logistics/
├── README.md
├── scripts/
│   ├── extract_airtable.py       # Extracts data from Airtable API (with rate limit handling)
│   ├── transform.py              # Cleans data, creates Cost per KG and Delivery Status
│   └── load_duckdb.py            # Loads clean data into DuckDB
├── notebooks/
│   └── EDA.ipynb                 # Exploratory Data Analysis - 4 data quality issues
└── data/
    └── shipments_1000.csv        # Raw subset (1000 rows) from USAID dataset
```

---

## Scripts

### 1. Extract from Airtable (`extract_airtable.py`)
- Uses `pyairtable` Python client
- Handles Airtable's **5 requests/sec rate limit** via `time.sleep(0.25)` between paginated requests
- Extracts all records and saves to `raw_shipments.csv`

### 2. Transform (`transform.py`)
- Standardizes `Shipment Mode` casing
- Parses date columns
- Calculates **Cost per KG** = `Freight Cost (USD)` / `Weight (Kilograms)`
- Creates **Delivery Status** = `On-Time` if delivered on or before scheduled date, else `Late`
- Drops rows with missing critical fields

### 3. Load to DuckDB (`load_duckdb.py`)
- Loads clean CSV into a local DuckDB database
- Table: `shipments`

---

## 🔗 Data Source
- **Dataset:** [USAID Supply Chain Shipment Pricing Data](https://www.kaggle.com/datasets/apoorvwatsky/supply-chain-shipment-pricing-data)
- **Records used:** 508 rows (subset of 10,000+)

---

## How to Run

```bash
# Install dependencies
pip install pandas pyairtable duckdb sqlalchemy psycopg2-binary

# Extract from Airtable
python scripts/extract_airtable.py

# Transform data
python scripts/transform.py

# Load to DuckDB
python scripts/load_duckdb.py
```

---

## Tech Stack
| Tool | Purpose |
|------|---------|
| Python + Pandas | Data extraction & transformation |
| PyAirtable | Airtable API client |
| DuckDB | Local analytical database |
| Supabase (PostgreSQL) | Cloud database for Preset connection |
| Preset.io / Apache Superset | Dashboard & visualization |
| GitHub | Version control & submission |
