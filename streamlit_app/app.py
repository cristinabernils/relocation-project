# streamlit_app/app.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from src.preprocessing import load_and_clean_indicator, get_common_year, aggregate_historical
from src.scoring import compute_relocation_score
from src.visuals import plot_dual_radar, plot_indicator_over_time
from src.predictive import predict_linear_trend, predict_random_forest_trend
from functools import reduce

st.set_page_config(page_title="Relocation Score App", layout="wide")

st.title("🌍 Data-Driven Relocation")
st.markdown("Set your priorities and discover the country that best matches your lifestyle.")

# --------------------------
# INITIAL CONFIGURATION
# --------------------------
INDICATORS = [
    "gdp_per_capita", "inflation", "unemployment",
    "gini_index", "education_spending_gdp"
]

CONTEXT_DATA = {
    "country": [
        "Germany", "Spain", "Norway", "United Kingdom",
        "Sweden", "Japan", "Portugal", "Greece"
    ],
    "maternity_score": [4, 4, 5, 3, 5, 2, 4, 3]
}
context_df = pd.DataFrame(CONTEXT_DATA)

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


# --------------------------
# WEIGHT SELECTION
# --------------------------
st.sidebar.header("🎛️ Prioritize what matters most to you")

w_gdp = st.sidebar.slider("Income (GDP per capita)", 0.0, 1.0, 0.3, 0.05)
w_gini = st.sidebar.slider("Equality (Gini index)", 0.0, 1.0, 0.2, 0.05)
w_edu = st.sidebar.slider("Education (% of GDP)", 0.0, 1.0, 0.15, 0.05)
w_mat = st.sidebar.slider("Maternity support", 0.0, 1.0, 0.1, 0.05)
w_emp = st.sidebar.slider("Employment (low unemployment)", 0.0, 1.0, 0.05, 0.01)
w_stab = st.sidebar.slider("Economic stability (low inflation)", 0.0, 1.0, 0.05, 0.01)
w_hdi = st.sidebar.slider("Human Development Index (HDI)", 0.0, 1.0, 0.3, 0.05)

# Normalize weights
total = sum([w_gdp, w_gini, w_edu, w_mat, w_emp, w_stab])
weights = {
    "gdp": w_gdp / total,
    "gini": w_gini / total,
    "education": w_edu / total,
    "maternity": w_mat / total,
    "employment": w_emp / total,
    "stability": w_stab / total,
    "hdi": w_hdi / total
}

# --------------------------
# LOAD DATA
# --------------------------
@st.cache_data
def load_data():
    dfs = []
    for ind in INDICATORS:
        path = os.path.join("data/raw", f"{ind}_worldbank.csv")
        df = load_and_clean_indicator(path, ind)
        dfs.append(df)
    merged = aggregate_historical(dfs)
    merged = pd.merge(merged, hdi_df, on=["country", "date"], how="left")
    return compute_relocation_score(merged, context_df, weights)

@st.cache_data
def load_historical_raw():
    dfs = []
    for ind in INDICATORS:
        path = os.path.join("data/raw", f"{ind}_worldbank.csv")
        df = load_and_clean_indicator(path, ind)
        dfs.append(df)
    merged = reduce(lambda l, r: pd.merge(l, r, on=["country", "country_code", "date"], how="outer"), dfs)
    return merged

df_scored = load_data()
df_raw = load_historical_raw()

# --------------------------
# FINAL RANKING + RECOMMENDATION
# --------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Country ranking based on your preferences")
    ranking = df_scored[["country", "relocation_score"]].sort_values(by="relocation_score", ascending=False)
    st.dataframe(ranking.set_index("country").style.format("{:.3f}"))

with col2:
    st.subheader("🧭 Personalized Recommendation")
    top3 = ranking.head(3)["country"].tolist()
    st.markdown(f"""
    **Top 3 recommended countries:**

    1. **{top3[0]}**  
    2. **{top3[1]}**  
    3. **{top3[2]}**
    """)
    reco = {
        "Norway": "Norway excels in social support, high salaries, and egalitarian policies.",
        "Sweden": "Sweden is balanced in all aspects, with progressive policies and strong quality of life.",
        "Germany": "Germany combines a strong economy with decent equality and job opportunities.",
        "United Kingdom": "UK has solid economic indicators, though weaker family policies.",
        "Japan": "Japan ranks high on GDP but lower in equality and maternity support.",
        "Portugal": "Portugal offers high quality of life and rights, with relatively lower salaries.",
        "Spain": "Spain is strong on maternity and social rights, with some challenges in employment.",
        "Greece": "Greece struggles more in employment and stability, despite a rich social culture."
    }
    top1 = top3[0]
    st.info(reco.get(top1, "This country leads your ranking by aligning well with your preferences."))

# --------------------------
# COUNTRY COMPARISON (RADAR)
# --------------------------
st.subheader("🕵️ Compare two countries side by side")
col_sel, col_chart = st.columns([1, 2])

with col_sel:
    cols = df_scored[["country"]].drop_duplicates().sort_values("country")["country"].tolist()
    c1 = st.selectbox("Country A", cols, index=0)
    c2 = st.selectbox("Country B", cols, index=1)

    st.markdown("""
    **Radar chart indicators:**
    - **GDP**: Income per capita.
    - **Education**: Education investment (% GDP).
    - **Equality**: Income equality (Gini index, inverted).
    - **Maternity**: Family support policies.
    - **Employment**: Inverted unemployment rate.
    - **Stability**: Economic stability (low inflation).
    - **HDI**: Human Development Index (UN)
    """)

with col_chart:
    comparison_df = df_scored.set_index("country")[[
        "gdp_per_capita", "education_spending_gdp", "gini_index_inverted",
        "maternity_score", "unemployment", "inflation", "hdi"
    ]].copy()
    comparison_df["unemployment"] = 1 - comparison_df["unemployment"]
    comparison_df["inflation"] = 1 - comparison_df["inflation"]
    comparison_df = comparison_df.rename(columns={
        "gdp_per_capita": "GDP",
        "education_spending_gdp": "Education",
        "gini_index_inverted": "Equality",
        "maternity_score": "Maternity",
        "unemployment": "Employment",
        "inflation": "Stability",
        "hdi": "HDI"
    })
    fig = plot_dual_radar(
        comparison_df.loc[c1],
        comparison_df.loc[c2],
        label1=c1,
        label2=c2
    )
    st.pyplot(fig)

# --------------------------
# HISTORICAL TREND + FORECAST
# --------------------------
st.subheader("📊 Historical evolution and forecast")
col_controls, col_graphs = st.columns([1, 2])

with col_controls:
    selected_country = st.selectbox("Select a country", sorted(df_raw["country"].unique()), index=0)
    indicator_to_predict = st.selectbox("Select an indicator", [
        "gdp_per_capita", "education_spending_gdp", "gini_index", "unemployment", "inflation"
    ])
    years_to_forecast = st.slider("Years to forecast", min_value=5, max_value=30, value=20)

with col_graphs:
    col_hist, col_pred = st.columns(2)

    with col_hist:
        fig_hist = plot_indicator_over_time(df_raw, selected_country, indicator_to_predict, ylabel=indicator_to_predict.replace("_", " ").title())
        fig_hist.set_size_inches(6, 4)
        st.pyplot(fig_hist)

    with col_pred:
        try:
            pred_df, model = predict_random_forest_trend(df_raw, selected_country, indicator_to_predict, years_to_forecast)
            fig_pred, ax = plt.subplots(figsize=(6, 4))
            sns.lineplot(
                x="date",
                y=indicator_to_predict,
                data=df_raw[df_raw["country"] == selected_country],
                label="Historical",
                ax=ax
            )
            sns.lineplot(
                x="year",
                y="prediction",
                data=pred_df,
                label="Forecast",
                ax=ax
            )
            ax.set_title(f"{indicator_to_predict} – {selected_country}")
            ax.set_xlabel("Year")
            ax.grid(True)
            st.pyplot(fig_pred)
        except Exception as e:
            st.warning(f"⚠️ Prediction could not be generated: {e}")