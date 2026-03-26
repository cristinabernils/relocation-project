# main.py
"""
CLI entry point for the Relocation App.
Downloads World Bank data and computes relocation scores.
"""

import os

import pandas as pd

from src.config import (
    CONTEXT_DATA,
    COUNTRIES,
    DATA_EXTERNAL_PATH,
    DATA_PROCESSED_PATH,
    DATA_RAW_PATH,
    DEFAULT_WEIGHTS,
    INDICATORS_DICT,
)
from src.data_fetching import fetch_multiple_indicators
from src.preprocessing import aggregate_historical, load_and_clean_indicator
from src.scoring import compute_relocation_score


# -----------------------------
# 1. Download World Bank data
# -----------------------------
def download_data():
    print("📥 Starting World Bank data download...")
    fetch_multiple_indicators(
        countries=COUNTRIES,
        indicators=INDICATORS_DICT,
        start_year=2003,
        end_year=2023
    )
    print("✅ World Bank data download complete!")

# -----------------------------
# 2. Process and score countries
# -----------------------------
def build_ranking():
    print("🔧 Building relocation score ranking...")

    INDICATORS = list(INDICATORS_DICT.values())
    dfs = []

    for ind in INDICATORS:
        path = os.path.join(DATA_RAW_PATH, f"{ind}_worldbank.csv")
        df = load_and_clean_indicator(path, ind)
        dfs.append(df)

    merged = aggregate_historical(dfs)

    # Load HDI external data and merge
    hdi_path = os.path.join(DATA_EXTERNAL_PATH, "hdi_historical.csv")
    hdi_df = pd.read_csv(hdi_path)
    hdi_df = hdi_df.rename(columns={
        "Entity": "country",
        "Year": "date",
        "Human Development Index": "hdi"
    })
    hdi_df["date"] = hdi_df["date"].astype(int)

    merged = pd.merge(merged, hdi_df, on=["country", "date"], how="left")

    # Contextual data from config
    context_df = pd.DataFrame(CONTEXT_DATA)

    # Default weight configuration from config
    weights = DEFAULT_WEIGHTS

    scored_df = compute_relocation_score(merged, context_df, weights)

    os.makedirs(DATA_PROCESSED_PATH, exist_ok=True)
    scored_df[["country", "relocation_score"]].sort_values(by="relocation_score", ascending=False)\
        .to_csv(f"{DATA_PROCESSED_PATH}relocation_ranking.csv", index=False)

    print("✅ Final ranking saved to data/processed/relocation_ranking.csv")

# -----------------------------
# Run full data pipeline
# -----------------------------
if __name__ == "__main__":
    download_data()
    build_ranking()
