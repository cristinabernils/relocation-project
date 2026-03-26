# main.py

from src.config import (
    CONTEXT_DATA,
    DEFAULT_WEIGHTS,
    DATA_RAW_PATH,
    DATA_PROCESSED_PATH,
    INDICATORS_DICT,
)
from src.data_fetching import fetch_multiple_indicators, EUROPE_ASIA_COUNTRIES
from src.preprocessing import load_and_clean_indicator, get_common_year, aggregate_historical
from src.scoring import compute_relocation_score

import pandas as pd
import os
from functools import reduce

# -----------------------------
# 1. Download World Bank data
# -----------------------------
def download_data():
    print("📥 Starting World Bank data download...")
    fetch_multiple_indicators(
        countries=EUROPE_ASIA_COUNTRIES,
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
    RAW_PATH = DATA_RAW_PATH
    dfs = []

    for ind in INDICATORS:
        path = os.path.join(RAW_PATH, f"{ind}_worldbank.csv")
        df = load_and_clean_indicator(path, ind)
        dfs.append(df)

    # Option: use a shared year (only if needed)
    # common_year = get_common_year(dfs)
    # if not common_year:
    #     raise Exception("❌ No common year found across all indicators.")
    # print(f"✅ Selected common year: {common_year}")
    # filtered = [df[df["date"] == common_year] for df in dfs]
    # merged = reduce(lambda l, r: pd.merge(l, r, on=["country", "country_code", "date"], how="inner"), filtered)

    merged = aggregate_historical(dfs)

    # Load HDI external data and merge
    hdi_path = os.path.join("data", "external", "hdi_historical.csv")
    hdi_df = pd.read_csv(hdi_path)
    hdi_df = hdi_df.rename(columns={
        "Entity": "country",
        "Year": "date",
        "Human Development Index": "hdi"
    })
    hdi_df["date"] = hdi_df["date"].astype(int) 
    hdi_df = hdi_df.rename(columns={"date": "date", "hdi": "hdi", "country": "country"})

    merged = aggregate_historical(dfs)
    merged = pd.merge(merged, hdi_df, on=["country", "date"], how="left")

    # Contextual data (non-numeric indicators)
    context_df = pd.DataFrame(CONTEXT_DATA)

    # Default weight configuration
    weights = DEFAULT_WEIGHTS

    scored_df = compute_relocation_score(merged, context_df, weights)

    os.makedirs(DATA_PROCESSED_PATH, exist_ok=True)
    scored_df[["country", "relocation_score"]].sort_values(by="relocation_score", ascending=False)\
        .to_csv(f"{DATA_PROCESSED_PATH}/relocation_ranking.csv", index=False)

    print("✅ Final ranking saved to data/processed/relocation_ranking.csv")

# -----------------------------
# Run full data pipeline
# -----------------------------
if __name__ == "__main__":
    download_data()
    build_ranking()
