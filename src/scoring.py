# src/scoring.py

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def compute_relocation_score(df, context_df, weights):
    df = df.merge(context_df, on="country", how="inner")
    
    # Invert gini
    df["gini_index_inverted"] = 1 - MinMaxScaler().fit_transform(df[["gini_index"]])
    
    # Normalize the rest
    to_normalize = [
        "gdp_per_capita", "education_spending_gdp",
        "unemployment", "inflation", "maternity_score", "hdi"
    ]
    df[to_normalize] = MinMaxScaler().fit_transform(df[to_normalize])
    
    df["relocation_score"] = (
        weights["gdp"] * df["gdp_per_capita"] +
        weights["gini"] * df["gini_index_inverted"] +
        weights["education"] * df["education_spending_gdp"] +
        weights["maternity"] * df["maternity_score"] +
        weights["employment"] * (1 - df["unemployment"]) +
        weights["stability"] * (1 - df["inflation"]) + 
        weights["hdi"] * df["hdi"]
    )
    
    return df