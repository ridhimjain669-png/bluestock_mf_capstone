
from pathlib import Path
import argparse
import sqlite3
import pandas as pd


FILES = {
    "fund_master": "fund_master_cleaned.csv",
    "nav": "nav_history_cleaned.csv",
    "transactions": "investor_transactions_cleaned.csv",
    "performance": "scheme_performance_cleaned.csv",
    "aum": "aum_cleaned.csv",
}

PERFORMANCE_COLUMNS = [
    "amfi_code", "return_1yr_pct", "return_3yr_pct",
    "return_5yr_pct", "benchmark_3yr_pct", "alpha", "beta",
    "sharpe_ratio", "sortino_ratio", "std_dev_ann_pct",
    "max_drawdown_pct", "aum_crore", "expense_ratio_pct",
    "morningstar_rating", "risk_grade",
]


def read_csv(input_dir, filename):
    path = input_dir / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")
    return pd.read_csv(path)


def clean_date_column(df, column):
    df[column] = pd.to_datetime(df[column], errors="coerce")
    if df[column].isna().any():
        raise ValueError(f"Invalid or missing dates found in column: {column}")
    df[column] = df[column].dt.strftime("%Y-%m-%d")
    return df


def create_tables(conn):
    conn.execute("PRAGMA foreign_keys = ON")

    conn.executescript("""
    CREATE TABLE IF NOT EXISTS dim_fund (
        amfi_code INTEGER PRIMARY KEY,
        fund_house TEXT,
        scheme_name TEXT,
        category TEXT,
        sub_category TEXT,
        plan TEXT,
        launch_date TEXT,
        benchmark TEXT,
        expense_ratio_pct REAL,
        exit_load_pct REAL,
        min_sip_amount REAL,
        min_lumpsum_amount REAL,
        fund_manager TEXT,
        risk_category TEXT,
        sebi_category_code TEXT
    );

    CREATE TABLE IF NOT EXISTS dim_date (
        date TEXT PRIMARY KEY,
        year INTEGER,
        month INTEGER,
        day INTEGER
    );

    CREATE TABLE IF NOT EXISTS fact_nav (
        amfi_code INTEGER,
        date TEXT,
        nav REAL,
        PRIMARY KEY (amfi_code, date),
        FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
        FOREIGN KEY (date) REFERENCES dim_date(date)
    );

    CREATE TABLE IF NOT EXISTS fact_transactions (
        investor_id TEXT,
        transaction_date TEXT,
        amfi_code INTEGER,
        transaction_type TEXT,
        amount_inr REAL,
        state TEXT,
        city TEXT,
        city_tier TEXT,
        age_group TEXT,
        gender TEXT,
        annual_income_lakh REAL,
        payment_mode TEXT,
        kyc_status TEXT,
        FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
        FOREIGN KEY (transaction_date) REFERENCES dim_date(date)
    );

    CREATE TABLE IF NOT EXISTS fact_performance (
        amfi_code INTEGER PRIMARY KEY,
        return_1yr_pct REAL,
        return_3yr_pct REAL,
        return_5yr_pct REAL,
        benchmark_3yr_pct REAL,
        alpha REAL,
        beta REAL,
        sharpe_ratio REAL,
        sortino_ratio REAL,
        std_dev_ann_pct REAL,
        max_drawdown_pct REAL,
        aum_crore REAL,
        expense_ratio_pct REAL,
        morningstar_rating REAL,
        risk_grade TEXT,
        FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
    );

    CREATE TABLE IF NOT EXISTS fact_aum (
        date TEXT,
        fund_house TEXT,
        aum_lakh_crore REAL,
        aum_crore REAL,
        num_schemes INTEGER,
        PRIMARY KEY (date, fund_house),
        FOREIGN KEY (date) REFERENCES dim_date(date)
    );
    """)


def main():
    parser = argparse.ArgumentParser(description="Load cleaned mutual fund CSVs into SQLite.")
    parser.add_argument("--input-dir", required=True, help="Folder containing cleaned CSV files")
    parser.add_argument("--db-path", required=True, help="Output SQLite database path")
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace an existing database file (use only when you intend to rebuild it)",
    )
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    db_path = Path(args.db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    if db_path.exists():
        if not args.replace:
            raise FileExistsError(
                f"Database already exists: {db_path}\n"
                "Choose a new path or add --replace if you intentionally want to rebuild it."
            )
        db_path.unlink()

    funds = read_csv(input_dir, FILES["fund_master"])
    nav = read_csv(input_dir, FILES["nav"])
    transactions = read_csv(input_dir, FILES["transactions"])
    performance = read_csv(input_dir, FILES["performance"])
    aum = read_csv(input_dir, FILES["aum"])

    for df in (funds, nav, transactions, performance, aum):
        df.columns = df.columns.str.strip()

    funds["launch_date"] = pd.to_datetime(
        funds["launch_date"], errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    nav = clean_date_column(nav, "date")
    transactions = clean_date_column(transactions, "transaction_date")
    aum = clean_date_column(aum, "date")

    for df, key in [
        (funds, "amfi_code"),
        (nav, "amfi_code"),
        (transactions, "amfi_code"),
        (performance, "amfi_code"),
    ]:
        df[key] = pd.to_numeric(df[key], errors="raise").astype("int64")

    known_funds = set(funds["amfi_code"])
    for label, df in [("NAV", nav), ("transactions", transactions),
                      ("performance", performance)]:
        missing = set(df["amfi_code"]) - known_funds
        if missing:
            raise ValueError(f"{label} contains AMFI codes missing from fund master: {sorted(missing)[:10]}")

    funds = funds.drop_duplicates(subset=["amfi_code"])
    nav = nav.drop_duplicates(subset=["amfi_code", "date"])
    transactions = transactions.drop_duplicates()
    performance = performance.drop_duplicates(subset=["amfi_code"])
    aum = aum.drop_duplicates(subset=["date", "fund_house"])

    dates = pd.concat([
        nav["date"],
        transactions["transaction_date"],
        aum["date"],
    ]).dropna().drop_duplicates()

    dim_date = pd.DataFrame({"date": dates})
    date_parts = pd.to_datetime(dim_date["date"])
    dim_date["year"] = date_parts.dt.year
    dim_date["month"] = date_parts.dt.month
    dim_date["day"] = date_parts.dt.day

    missing_performance_columns = [
        col for col in PERFORMANCE_COLUMNS if col not in performance.columns
    ]
    if missing_performance_columns:
        raise ValueError(f"Performance CSV is missing columns: {missing_performance_columns}")

    performance = performance[PERFORMANCE_COLUMNS]

    with sqlite3.connect(db_path) as conn:
        create_tables(conn)

        funds.to_sql("dim_fund", conn, if_exists="append", index=False)
        dim_date.to_sql("dim_date", conn, if_exists="append", index=False)
        nav.to_sql("fact_nav", conn, if_exists="append", index=False)
        transactions.to_sql("fact_transactions", conn, if_exists="append", index=False)
        performance.to_sql("fact_performance", conn, if_exists="append", index=False)
        aum.to_sql("fact_aum", conn, if_exists="append", index=False)

        print("\nETL completed. Rows loaded:")
        for table in [
            "dim_fund", "dim_date", "fact_nav",
            "fact_transactions", "fact_performance", "fact_aum"
        ]:
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"{table}: {count:,}")


if __name__ == "__main__":
    main()
