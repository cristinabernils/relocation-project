import os
import requests
import pandas as pd

os.makedirs("data/raw", exist_ok=True)

# 🌍 List of countries: Europe, Asia, and the UK
EUROPE_ASIA_COUNTRIES = [
    "DEU", "FRA", "ITA", "ESP", "NLD", "SWE", "POL", "GRC", "PRT", "NOR",
    "GBR",  # UK
    "JPN", "KOR", "CHN", "IND", "SGP", "VNM"
]

# 📊 World Bank Indicators: {api_code: file_name}
INDICATORS_DICT = {
    "NY.GDP.PCAP.CD": "gdp_per_capita",                  # GDP per capita (USD)
    "FP.CPI.TOTL.ZG": "inflation",                       # Inflation (annual %)
    "SL.UEM.TOTL.ZS": "unemployment",                    # Unemployment rate (%)
    "SP.POP.TOTL": "population",                          # Total population
    "SI.POV.GINI": "gini_index",                         # Gini index (inequality)
    "SE.XPD.TOTL.GD.ZS": "education_spending_gdp"        # Education spending (% of GDP)
}

# 🏦 Base function for a single indicator and country
def fetch_world_bank_data(indicator, countries, start_year=2003, end_year=2023):
    """
    Downloads data from the World Bank for a given indicator and list of countries.

    Returns:
        pd.DataFrame with columns: country, country_code, date, value
    """
    all_data = []

    for country in countries:
        url = f"http://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
        params = {
            "format": "json",
            "date": f"{start_year}:{end_year}",
            "per_page": 1000
        }
        response = requests.get(url, params=params)
        data = response.json()

        if not data or len(data) < 2:
            print(f"No data for {country} - {indicator}")
            continue

        for entry in data[1]:
            all_data.append({
                "country": entry["country"]["value"],
                "country_code": country,
                "date": entry["date"],
                "value": entry["value"]
            })

    return pd.DataFrame(all_data)


# 🔁 Function to fetch multiple indicators
def fetch_multiple_indicators(countries, indicators, start_year=2003, end_year=2023):
    """
    Downloads and saves multiple indicators from the World Bank for several countries.
    """
    for indicator_code, name in indicators.items():
        print(f"Fetching: {name}")
        df = fetch_world_bank_data(indicator_code, countries, start_year, end_year)
        df.to_csv(f"data/raw/{name}_worldbank.csv", index=False)
        print(f"Saved: data/raw/{name}_worldbank.csv")