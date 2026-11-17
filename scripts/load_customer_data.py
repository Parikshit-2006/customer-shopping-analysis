"""Clean customer.csv and load it into MySQL (phpMyAdmin / MAMP compatible)."""
from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

ROOT = Path(__file__).resolve().parents[1]
INPUT = Path(os.getenv("CUSTOMER_CSV", ROOT / "data" / "customer.csv"))


def main() -> None:
    if not INPUT.exists():
        raise FileNotFoundError(
            f"Dataset not found at {INPUT}. Put customer.csv in data/ or set CUSTOMER_CSV."
        )
    df = pd.read_csv(INPUT)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)

    # Supports both the processed supplied file and the original Kaggle-style column name.
    df = df.rename(columns={"purchase_amount_(usd)": "purchase_amt"})
    if "purchase_amt" not in df.columns:
        raise ValueError("Expected purchase_amt or purchase_amount_(usd) in the CSV.")

    if "review_rating" in df.columns:
        df["review_rating"] = pd.to_numeric(df["review_rating"], errors="coerce")
        df["review_rating"] = df.groupby("category")["review_rating"].transform(
            lambda values: values.fillna(values.median())
        )

    if "age_group" not in df.columns:
        labels = ["young_adult", "adult", "middle-aged", "senior"]
        df["age_group"] = pd.qcut(df["age"], q=4, labels=labels)

    frequency_days = {
        "Weekly": 7, "Bi-Weekly": 14, "Fortnightly": 14, "Monthly": 30,
        "Quarterly": 90, "Every 3 Months": 90, "Annually": 365,
    }
    if "purchase_frequency_days" not in df.columns:
        df["purchase_frequency_days"] = df["frequency_of_purchases"].map(frequency_days)

    # promo_code_used duplicates discount_applied in the original source and is not needed.
    df = df.drop(columns=["promo_code_used"], errors="ignore")

    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "root")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "8889")
    database = os.getenv("DB_NAME", "customer_behavior")
    table = os.getenv("DB_TABLE", "customer")
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
    df.to_sql(table, engine, if_exists="replace", index=False)
    print(f"Loaded {len(df):,} rows into {database}.{table}.")


if __name__ == "__main__":
    main()
