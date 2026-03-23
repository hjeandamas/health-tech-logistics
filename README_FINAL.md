# **Prepared: Jean Damascene HAGENIMANA**
# *Email: hjeandamas@gmail.com*
# *Tel: 0788284928*

# Health-Tech Logistics: End-to-End Supply Chain Analytics Pipeline

## Project Summary
This repository contains my submission for the **Health-Tech Logistics technical challenge**. I built an end-to-end analytics workflow that starts with raw health commodity shipment data, stages it in Airtable, transforms it into an analytics-ready dataset, and publishes a business-facing dashboard in **Preset / Apache Superset**.

The objective of the solution is to help a logistics team answer three practical questions:
- Where are freight costs highest?
- How consistent is delivery performance over time?
- Which shipment decisions are driving avoidable cost?

The final output is a dashboard designed for decision-makers responsible for delivery efficiency and cost optimization across vaccine and medication supply chains.

---

## Challenge Scope Covered
The assignment requested three main components, and I structured the solution accordingly.

### Part 1: Data Ingestion & Engineering (Raw Stage)
- Selected and prepared a subset of the **USAID Supply Chain Shipment Pricing Dataset** from Kaggle
- Imported the subset into an **Airtable base**
- Extracted the Airtable records programmatically using Python
- Demonstrated awareness of Airtable API constraints, including the **5 requests/second rate limit**
- Loaded transformed data into analytical storage layers for validation and visualization

### Part 2: Data Quality & Transformation (Logic Stage)
- Assessed the raw shipment data for quality issues
- Standardized key categorical values
- Parsed date and numeric fields
- Engineered operational features such as **Cost per KG** and **Delivery Status**
- Prepared a cleaned dataset for downstream analytics

### Part 3: Dashboard & Business Narrative (Impact Stage)
- Built an interactive dashboard in **Preset / Apache Superset**
- Focused the dashboard on delivery performance and cost optimization
- Framed the charts to support operational decision-making rather than descriptive reporting alone

---

## Data Source
- **Dataset:** USAID Supply Chain Shipment Pricing Data
- **Source:** Kaggle
- **Use case:** Health commodity shipments, freight cost, shipment mode, delivery timelines, and related logistics attributes

For this challenge, I worked with a subset of the full dataset and staged it through Airtable before processing it downstream.

---

## Solution Architecture

```text
USAID Shipment Dataset (Kaggle)
            ↓
Prepared shipment subset
            ↓
Airtable Base (raw operational layer)
            ↓
Python extraction from Airtable API
            ↓
Pandas cleaning and feature engineering
            ↓
DuckDB (local validation layer)
            ↓
Supabase PostgreSQL (serving layer)
            ↓
Preset / Apache Superset Dashboard
```

### Why this design?
I used this architecture to reflect a realistic lightweight analytics workflow:
- **Airtable** simulates an operational data-entry or vendor-submission layer
- **Python + Pandas** handle extraction, validation, and transformation
- **DuckDB** provides fast local validation and easy SQL-based inspection
- **Supabase PostgreSQL** serves as a hosted backend for visualization tools
- **Preset / Superset** turns the cleaned data into an executive-facing dashboard

---

## Raw Stage: Airtable Ingestion and Extraction
I prepared a shipment subset and loaded it into Airtable to match the challenge requirement of beginning from an Airtable-tracked source.

### What I implemented
- Imported a shipment subset into Airtable
- Extracted records with Python using the Airtable API
- Iterated through paginated responses
- Stored the extracted result as a raw CSV for downstream processing

### Airtable rate-limit handling
Airtable enforces a limit of **5 requests per second per base**. To stay within that limit, I added controlled pacing to the extraction step using:

```python
import time
...
time.sleep(0.25)
```

This simple pacing strategy keeps requests below the threshold and is appropriate for a challenge-scale batch sync.

### Data integrity approach
In the submitted workflow, I included several practical integrity checks:
- preserved a **raw extract** before any transformation
- separated raw and cleaned outputs
- applied explicit type conversion for key numeric columns
- parsed date columns deliberately instead of relying on implicit typing
- validated row counts after loading into analytical storage

### What I would add in production
To harden this for a production environment, I would extend it with:
- retry logic with exponential backoff
- idempotent upserts instead of replace-only loads
- schema validation before insert
- record-level deduplication
- logging and load audit tables

---

## Data Quality Assessment
Before transformation, I performed exploratory checks on the extracted Airtable data.

### Key issues identified
1. **Missing values**  
   Important fields such as delivery dates, freight costs, and shipment weight contained missing values that would affect delivery-performance and cost analysis.

2. **Outliers**  
   Freight cost and shipment weight showed extreme values that could distort averages and comparative metrics.

3. **Inconsistent categorical values**  
   Shipment mode values required standardization to ensure consistent grouping and reporting.

4. **Invalid values for calculations**  
   Some records had missing, zero, or unusable numeric values in fields needed for cost-per-kilogram calculations.

These issues were important because the final dashboard depends on reliable dates, standardized shipment modes, and usable freight/weight values.

---

## Transformation Logic
I cleaned and enriched the dataset to make it analysis-ready.

### Core transformations
- standardized `Shipment Mode`
- converted `Freight Cost (USD)`, `Weight (Kilograms)`, and `Line Item Value` to numeric fields
- parsed `Scheduled Delivery Date` and `Delivered to Client Date`
- created an analytical subset by removing rows missing the fields required for the dashboard metrics: `Freight Cost (USD)`, `Weight (Kilograms)`, and `Delivered to Client Date`

### Important note on Shipment Mode in the dashboard
The raw dataset contained more than one shipment mode. However, the dashboard was built on the cleaned analytical dataset after applying completeness filters to ensure that cost and delivery metrics were calculated on valid records only.

As a result, some shipment-mode categories present in the raw data did not remain in the final dashboard dataset because they had missing values in one or more required fields. In this subset, the remaining records that satisfied the analytical criteria were all labeled **Air**. Therefore, the dashboard showing only **Air** under `Shipment Mode` reflects the effect of data-quality filtering, **not** a manual exclusion of other shipment modes such as `Truck`.

### Derived features
- **Cost per KG** = `Freight Cost (USD)` / `Weight (Kilograms)`
- **Delivery Status** = `On-Time` if actual delivery date is on or before scheduled delivery date, otherwise `Late`

These engineered fields are central to the business narrative because they translate raw shipment logs into indicators of **cost efficiency** and **service reliability**.

### Analytical implication
This cleaning choice improved metric reliability for the challenge dashboard, but it also narrowed the shipment-mode comparison in the final visualization. In a production setting, I would preserve a broader mode-complete dataset for descriptive shipment-mode analysis and use a stricter subset only for metrics that require complete freight and weight information.

---

## Analytical Storage
I used two storage layers in the workflow:

### DuckDB
DuckDB served as a lightweight local analytical database for validation and quick querying after transformation.

### Supabase PostgreSQL
I then pushed the cleaned dataset to Supabase PostgreSQL so it could be connected directly to Preset / Superset for dashboard development and sharing.

This separation allowed me to validate the cleaned data locally before publishing it through a hosted analytics layer.

---

## Dashboard
**Live dashboard:**  
https://f60043fb.us1a.app.preset.io/superset/dashboard/8/?native_filters_key=ZZRyZzJ6Ttc

The dashboard was designed to communicate a clear operational story rather than present disconnected charts.

### 1) Total Shipments
A headline KPI shows the volume of shipments included in the analytical dataset and gives decision-makers a quick sense of the reporting scope.

### 2) Average Freight Cost by Country
This view highlights geographies where average freight cost is materially higher. It supports questions such as:
- Which lanes are most expensive?
- Where should vendor or route reviews begin?
- Which countries may benefit from shipment consolidation?

### 3) On-Time Delivery Trend
This chart shows delivery consistency over time and helps identify volatility, delays, or possible bottlenecks in the logistics process.

### 4) Cost per KG by Shipment Mode
This view was designed to support cost optimization by comparing shipment modes on a normalized basis. In the current challenge dataset, only **Air** appears in the final dashboard because the cleaned analytical dataset retained only records with complete freight, weight, and delivery information. Other shipment modes existed in the raw data but were excluded by data-completeness filtering rather than by manual selection.

---

## Business Interpretation
The dashboard supports a practical supply chain decision framework:

- **High-cost countries** may require route redesign, negotiation, or consolidation strategies
- **Delivery variability over time** may indicate operational bottlenecks or inconsistent planning
- **Higher cost per kilogram for premium shipment modes** suggests those modes should be reserved for urgent or lightweight shipments

### Working hypothesis
A key analytical hypothesis in this project is:

> Air shipments are less cost-effective than lower-cost transport modes for heavier loads, even when they may provide better speed or service reliability.

The dashboard was structured to provide evidence relevant to this hypothesis, while also acknowledging that the current analytical subset limits direct mode-to-mode comparison.

---

## Repository Structure
```text
health-tech-logistics/
├── README.md
├── notebooks/
│   └── Damascene Healt tech logistic Notebook.ipynb
├── data/
│   ├── raw_shipments.csv
│   └── shipments_clean.csv
├── scripts/
│   ├── extract_airtable.py
│   ├── transform.py
│   └── load_duckdb.py
└── dashboard/
    └── dashboard_link.txt
```

> Depending on how the project is packaged, some script logic may also appear directly in the notebook used during development.

---

## How to Reproduce the Workflow
### 1. Install dependencies
```bash
pip install pandas numpy pyairtable duckdb sqlalchemy psycopg2-binary matplotlib seaborn
```

### 2. Prepare the source subset
- Download the shipment dataset from Kaggle
- Create the working subset for the challenge
- Import that subset into Airtable

### 3. Extract from Airtable
Run the Airtable extraction logic to pull records into a raw CSV.

### 4. Clean and engineer features
Run the transformation logic to standardize fields, parse dates, derive metrics, and save the cleaned output.

### 5. Load the cleaned data
- validate locally in DuckDB
- publish the cleaned table to Supabase PostgreSQL

### 6. Build the dashboard
Connect Preset / Superset to the hosted PostgreSQL table and create the dashboard views.

---

## Tools and Technologies
| Tool | Role in the solution |
|------|----------------------|
| Python | ETL orchestration and analysis |
| Pandas | Cleaning, typing, and feature engineering |
| Airtable API / PyAirtable | Raw data extraction |
| DuckDB | Local validation and analytics |
| Supabase PostgreSQL | Hosted serving layer |
| Preset / Apache Superset | Dashboarding and business storytelling |
| Matplotlib / Seaborn | Exploratory data analysis |
| GitHub | Version control and submission |

---

## Strengths of the Submission
- End-to-end workflow from raw operational data to dashboard
- Clear alignment with the challenge structure
- Practical handling of Airtable API limits
- Business-oriented dashboard narrative
- Use of both local and hosted storage layers
- Feature engineering directly tied to delivery efficiency and cost analysis
- Transparent documentation of how cleaning decisions affect analytical outputs

---

## Limitations and Next Steps
### Current limitations
- The current implementation is optimized for challenge delivery rather than full production packaging
- Rate-limit handling is intentionally simple and could be extended with robust retry logic
- Validation rules can be expanded further for enterprise-grade pipelines
- The workflow would benefit from parameterization and orchestration for repeat runs
- The current dashboard subset is stricter than the raw dataset and therefore does not preserve all shipment modes for comparison

### Recommended next steps
- package the workflow into reusable modular scripts
- add structured logging and audit tables
- implement schema tests and deduplication checks
- create separate analytical layers for completeness-sensitive metrics versus broader descriptive reporting
- extend the dashboard with SLA compliance, route-level analysis, and vendor performance metrics

---

## Confidentiality and Configuration Note
In a production-ready version of this repository, API tokens, database credentials, and connection strings should be stored in environment variables or a `.env` file and excluded from version control.

---

## Closing Note
This project demonstrates how I approach a real-world analytics problem end to end: ingesting semi-structured operational data, validating and transforming it into a reliable analytical layer, and presenting the output in a way that supports business action. The final solution is intentionally practical, lightweight, and decision-focused.
