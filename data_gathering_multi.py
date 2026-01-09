import pandas as pd
from datetime import datetime

def get_prices():
    # Placeholder: Replace with real API calls (yfinance, crypto, etc.)
    assets = ["BTC", "AAPL"]
    data = pd.DataFrame({
        "Time": pd.date_range(start=datetime.now(), periods=10, freq="T"),
        "BTC": [31000, 31100, 31050, 31200, 31150, 31300, 31250, 31400, 31350, 31500],
        "AAPL": [150, 151, 150.5, 152, 151.5, 153, 152.5, 154, 153.5, 155]
    })
    return data
