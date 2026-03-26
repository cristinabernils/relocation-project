# src/config.py
"""
Centralized configuration for the Relocation App.
All shared constants, country lists, and static data live here.
"""

# List of countries: Europe, Asia, and the UK
COUNTRIES = [
    "DEU",  # Germany
    "FRA",  # France
    "ITA",  # Italy
    "ESP",  # Spain
    "NLD",  # Netherlands
    "SWE",  # Sweden
    "POL",  # Poland
    "GRC",  # Greece
    "PRT",  # Portugal
    "NOR",  # Norway
    "GBR",  # United Kingdom
    "JPN",  # Japan
    "KOR",  # South Korea
    "CHN",  # China
    "IND",  # India
    "SGP",  # Singapore
    "VNM",  # Vietnam
]

# World Bank Indicators: {api_code: file_name}
INDICATORS_DICT = {
    "NY.GDP.PCAP.CD": "gdp_per_capita",                  # GDP per capita (USD)
    "FP.CPI.TOTL.ZG": "inflation",                       # Inflation (annual %)
    "SL.UEM.TOTL.ZS": "unemployment",                   # Unemployment rate (%)
    "SP.POP.TOTL": "population",                         # Total population
    "SI.POV.GINI": "gini_index",                         # Gini index (inequality)
    "SE.XPD.TOTL.GD.ZS": "education_spending_gdp"       # Education spending (% of GDP)
}

INDICATORS = [
    "gdp_per_capita",
    "inflation",
    "unemployment",
    "gini_index",
    "education_spending_gdp"
]

# Context data - non-World Bank indicators
# Maternity score: 1-5 scale (5 = best family/work-life balance policies)
# TODO: Find a real data source for this
CONTEXT_DATA = {
    "country": [
        "Germany",
        "Spain",
        "Norway",
        "United Kingdom",
        "Sweden",
        "Japan",
        "Portugal",
        "Greece"
    ],
    "maternity_score": [4, 4, 5, 3, 5, 2, 4, 3]
}

# Default weights for relocation score
DEFAULT_WEIGHTS = {
    "gdp": 0.30,
    "gini": 0.20,
    "education": 0.15,
    "maternity": 0.10,
    "employment": 0.05,
    "stability": 0.05,
    "hdi": 0.15
}

# Data paths
DATA_RAW_PATH = "data/raw/"
DATA_PROCESSED_PATH = "data/processed/"
DATA_EXTERNAL_PATH = "data/external/"

# Country recommendations (used in Streamlit app)
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
