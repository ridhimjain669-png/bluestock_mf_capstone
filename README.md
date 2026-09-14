# Mutual Fund Analytics Platform

## Project Overview

The Mutual Fund Analytics Platform was developed as part of the Bluestock Fintech Data Analyst Internship.

The project brings together mutual fund scheme information, Net Asset Value (NAV), Assets Under Management (AUM), SIP inflows, investor transactions, portfolio holdings, and benchmark index data.

The objective is to organise and analyse this data to explore industry trends, fund performance, risk measures, investor transaction patterns, and benchmark comparisons.

## Project Objectives

* Prepare and validate mutual fund and market-related datasets.
* Build a reusable Python ETL pipeline.
* Store structured data in a SQLite database using a star schema.
* Use SQL queries and Python notebooks for analysis.
* Develop dashboards to present key findings and trends.
* Document the workflow and project limitations.

## Data Sources

The project uses datasets relating to:

* Mutual fund scheme details
* Historical NAV
* Fund-house AUM
* SIP inflows and accounts
* Category-wise inflows
* Investor transactions
* Portfolio holdings
* Benchmark indices
* Scheme performance metrics
* Folio trends

The capstone brief identifies sources such as AMFI India, mfapi.in, mfdata.in, NSE India, and BSE India.

**Data note:** Some information is based on public sources. NAV data includes simulated forward observations, and investor transaction data is synthetic. Findings from synthetic data describe the project dataset and should not be interpreted as actual investor behaviour.

## Tools and Technologies

* Python
* Pandas
* SQLite
* SQL
* Jupyter Notebook / Google Colab
* Power BI
* Tableau
* Git and GitHub

## Project Structure

```text
bluestock_mf_capstone/
├── data/
│   ├── raw/
│   ├── processed/
│   └── db/
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda_analysis.ipynb
│   ├── 04_performance_analytics.ipynb
│   └── 05_advanced_analytics.ipynb
├── scripts/
│   ├── etl_pipeline.py
│   ├── live_nav_fetch.py
│   ├── compute_metrics.py
│   └── recommender.py
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── dashboard/
│   └── bluestock_mf.pbix
├── reports/
│   ├── Final_Report.pdf
│   └── Presentation.pptx
└── README.md
```

## ETL Pipeline

The reusable ETL script is located at:

`scripts/etl_pipeline.py`

The pipeline prepares the datasets and loads the structured data into SQLite.

### Main steps

1. Read the source datasets.
2. Clean and validate the data.
3. Prepare the required fields and data types.
4. Load the data into the SQLite database.
5. Check the loaded table row counts.

The ETL pipeline was tested using a separate SQLite test database. The test load included:

| Table               | Rows loaded |
| ------------------- | ----------: |
| `dim_fund`          |          40 |
| `dim_date`          |       1,297 |
| `fact_nav`          |      46,000 |
| `fact_transactions` |      32,778 |
| `fact_performance`  |          40 |
| `fact_aum`          |          90 |

## Database Design

The project uses a SQLite database and a star-schema structure.

The schema includes dimension tables for funds and dates, along with fact tables for NAV, transactions, performance, and AUM.

The main database file is:

`data/db/bluestock_mf.db`

The database file may not be included in the GitHub repository. If it is excluded, the schema and ETL script provide the information needed to recreate it.

## Analysis

The analysis covers:

* Exploratory Data Analysis (EDA)
* NAV and AUM trends
* SIP and category inflow trends
* Investor transaction patterns
* Folio trends
* Fund performance and risk measures
* Correlation between selected funds
* Comparisons with benchmark indices

Performance measures include CAGR, Sharpe ratio, Sortino ratio, alpha, beta, and maximum drawdown. A weighted fund scorecard is also used to compare selected schemes.

**Important limitation:** The NAV history does not provide a complete five-year period for every scheme. Five-year CAGR results should therefore be interpreted with this limitation in mind.

## Dashboards

The project includes dashboards covering four areas:

1. **Industry Overview** — industry-level AUM, SIP, folio, and related trends.
2. **Fund Performance** — fund performance, risk measures, and benchmark comparisons.
3. **Investor Analytics** — transaction patterns across selected investor attributes.
4. **SIP & Market Trends** — SIP activity and market-related trends.

The dashboards support interactive exploration through filters and slicers.

## How to Run

1. Clone or download the GitHub repository.
2. Install the Python packages required by the notebooks and scripts.
3. Place the source datasets in the expected project data folder.
4. Run the ETL pipeline using the instructions and file paths in the script.
5. Open the analysis notebooks in Jupyter Notebook or Google Colab.
6. Open the dashboard files using the appropriate BI application.

## Limitations

* Some NAV observations are simulated.
* Investor transaction data is synthetic.
* The analysis depends on the completeness and quality of the supplied datasets.
* Five-year CAGR may not be available for every scheme.
* The project is intended for educational and analytical purposes and is not financial advice.

## Author

**Ridhi M. Jain**
Data Analyst Intern — Bluestock Fintech
B.Com (Finance & Taxation) Student

## Acknowledgement

This project was completed as part of the Bluestock Fintech Data Analyst Internship.
