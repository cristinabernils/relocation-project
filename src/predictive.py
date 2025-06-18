from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd

def predict_linear_trend(df, country, indicator, years_ahead=20):
    """
    Predicts future trend using linear regression.
    """
    country_df = df[df["country"] == country].sort_values("date")
    X = country_df["date"].values.reshape(-1, 1)
    y = country_df[indicator].values

    model = LinearRegression()
    model.fit(X, y)

    future_years = np.arange(X[-1][0] + 1, X[-1][0] + years_ahead + 1).reshape(-1, 1)
    predictions = model.predict(future_years)

    pred_df = pd.DataFrame({
        "year": future_years.flatten(),
        "prediction": predictions
    })
    return pred_df, model

def predict_random_forest_trend(df, country, indicator, years_ahead=20):
    """
    Predicts future trend using Random Forest Regressor.
    """
    country_df = df[df["country"] == country].sort_values("date")
    X = country_df["date"].values.reshape(-1, 1)
    y = country_df[indicator].values

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    future_years = np.arange(X[-1][0] + 1, X[-1][0] + years_ahead + 1).reshape(-1, 1)
    predictions = model.predict(future_years)

    pred_df = pd.DataFrame({
        "year": future_years.flatten(),
        "prediction": predictions
    })
    return pred_df, model