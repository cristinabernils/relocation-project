# src/preprocessing.py

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def load_and_clean_indicator(path, indicator_name):
    df = pd.read_csv(path)
    df["date"] = pd.to_numeric(df["date"], errors="coerce")
    df = df.rename(columns={"value": indicator_name})
    
    # Imputation using country-level mean
    df[indicator_name] = df.groupby("country")[indicator_name].transform(lambda x: x.fillna(x.mean()))
    # If NaNs remain → use global yearly median
    df[indicator_name] = df.groupby("date")[indicator_name].transform(lambda x: x.fillna(x.median()))
    
    return df.dropna(subset=[indicator_name])

def get_common_year(dfs):
    common_years = set(dfs[0]["date"].unique())
    for df in dfs[1:]:
        common_years &= set(df["date"].unique())
    return max(common_years) if common_years else None

def aggregate_historical(dfs):
    """
    Merges and averages multiple indicators per country over time.
    """
    from functools import reduce

    df_merged = reduce(
        lambda l, r: pd.merge(l, r, on=["country", "country_code", "date"], how="outer"),
        dfs
    )

    # Take the average of each indicator per country
    df_avg = df_merged.groupby(["country", "country_code"], as_index=False).mean(numeric_only=True)
    return df_avg