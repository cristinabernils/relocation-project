# 🌍 Data-Driven Relocation App

This project is an interactive tool designed to help professionals evaluate and compare countries for potential relocation based on macroeconomic, social, and developmental indicators.

Built using **Python, Streamlit, Pandas, and Scikit-learn**, it integrates data from the **World Bank** and **Human Development Index (HDI)** to provide a personalized relocation ranking based on user preferences.

---

## 📌 Project Highlights

- **Personalized country ranking** based on weighted criteria (salary, equality, education, etc.)
- **Comparative radar plots** between countries
- **Time-series forecasts** of key indicators using Random Forest
- Real data from World Bank & UN (HDI historical values 2003–2023)
- Deployed as an interactive Streamlit app

---

## 🔍 Key Indicators

The following variables are used to evaluate countries:

| Indicator                   | Source        | Description                                         |
|-----------------------------|---------------|-----------------------------------------------------|
| GDP per capita              | World Bank    | Proxy for salary and economic development           |
| Gini index                  | World Bank    | Measures income inequality                          |
| Inflation rate              | World Bank    | Indicator of economic stability                     |
| Unemployment rate           | World Bank    | Employment health                                   |
| Education spending (% GDP) | World Bank    | Investment in education                             |
| Maternity score             | Manual        | Proxy for family/work-life balance policies         |
| HDI                         | UNDP          | Human Development Index (historical, 2003–2023)     |

---

## 🧠 How It Works

1. **Data collection**  
   Data is fetched from the World Bank API and HDI data is loaded from a curated historical dataset.

2. **Scoring**  
   Indicators are cleaned, normalized, and weighted using user input. A relocation score is computed per country.

3. **Visualization**  
   The app presents:
   - Country rankings
   - Radar comparison between two countries
   - Historical trends and indicator forecasts

4. **Prediction**  
   Forecasts are generated using a **Random Forest Regressor**, trained on available time series data (2003–2023).

---

## 🚀 Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/your_username/relocation-app.git
cd relocation-app
```

### 2. Set up the environment

You can use either `conda` or a virtual environment.

#### Option 1: Using Conda (recommended)

```bash
conda env create -f environment.yml
conda activate relocation-env
```

#### Option 2: Using virtualenv + pip

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

### 3. Run the project

#### Fetch and process the data

```bash
python main.py
```

This will download World Bank indicators and compute relocation scores.

#### Launch the app

```bash
streamlit run streamlit_app/app.py
```

This will open the interactive dashboard in your browser at `http://localhost:8501`.

---

## 📁 Project Structure

```
relocation-app/
│
├── data/                   # Raw and processed data
│   ├── raw/
│   ├── processed/
│   └── external/
│
├── notebooks/              # EDA and model experimentation
│
├── scripts/                # Utilities (e.g., web scraping HDI)
│
├── src/                    # Main Python modules (ETL, scoring, plotting)
│
├── streamlit_app/          # Streamlit dashboard
│
├── main.py                 # Pipeline entrypoint (download + process data)
├── requirements.txt        # pip dependencies
├── environment.yml         # conda environment
└── README.md
```

## 👩‍💻 About this project

This project was born from a personal curiosity: how can data help us decide where to live?  
It combines my interest in data science with social development and global mobility.  

🧠 Through this project I improved my skills in:
- Building data pipelines from APIs (World Bank)
- Data cleaning, feature engineering and scoring logic
- Time series forecasting with Random Forest
- App development with Streamlit for non-technical users