# src/config.py
# Centralized configuration constants for the relocation project

# 🌍 List of countries: Europe, Asia, and the UK
COUNTRIES = [
    "Germany", "Spain", "Norway", "United Kingdom",
    "Sweden", "Japan", "Portugal", "Greece"
]

# 📊 World Bank Indicators: {api_code: file_name}
INDICATORS_DICT = {
    "NY.GDP.PCAP.CD": "gdp_per_capita",  # GDP per capita (USD)
    "FP.CPI.TOTL.ZG": "inflation",  # Inflation (annual %)
    "SL.UEM.TOTL.ZS": "unemployment",  # Unemployment rate (%)
    "SP.POP.TOTL": "population",  # Total population
    "SI.POV.GINI": "gini_index",  # Gini index (inequality)
    "SE.XPD.TOTL.GD.ZS": "education_spending_gdp"  # Education spending (% of GDP)
}

# 📊 List of indicator names (values from INDICATORS_DICT)
INDICATORS = list(INDICATORS_DICT.values())

# 📋 Contextual data (non-numeric indicators)
CONTEXT_DATA = {
    "country": [
        "Germany", "Spain", "Norway", "United Kingdom",
        "Sweden", "Japan", "Portugal", "Greece"
    ],
    "maternity_score": [4, 4, 5, 3, 5, 2, 4, 3]
}

# ⚖️ Default weight configuration for scoring algorithm
DEFAULT_WEIGHTS = {
    "gdp": 0.30,
    "gini": 0.20,
    "education": 0.15,
    "maternity": 0.10,
    "employment": 0.05,
    "stability": 0.05,
    "hdi": 0.15
}

# 📂 Data paths
DATA_RAW_PATH = "data/raw/"
DATA_EXTERNAL_PATH = "data/external"
DATA_PROCESSED_PATH = "data/processed"

# 💬 Country recommendations
COUNTRY_RECOMMENDATIONS = {
    "Norway": "Norway excels in social support, high salaries, and egalitarian policies.",
    "Sweden": "Sweden is balanced in all aspects, with progressive policies and strong quality of life.",
    "Germany": "Germany combines a strong economy with decent equality and job opportunities.",
    "United Kingdom": "UK has solid economic indicators, though weaker family policies.",
    "Japan": "Japan ranks high on GDP but lower in equality and maternity support.",
    "Portugal": "Portugal offers high quality of life and rights, with relatively lower salaries.",
    "Spain": "Spain is strong on maternity and social rights, with some challenges in employment.",
    "Greece": "Greece struggles more in employment and stability, despite a rich social culture."
}
