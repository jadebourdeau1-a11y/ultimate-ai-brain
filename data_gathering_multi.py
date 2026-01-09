import yfinance as yf
import pandas as pd
from datetime import datetime

def get_live_price(ticker):
    data = yf.Ticker(ticker)
    price = data.history(period="1m").iloc[-1]['Close']
    return price

def get_portfolio_prices(tickers):
    prices = {}
    for t in tickers:
        try:
            prices[t] = get_live_price(t)
        except Exception:
            prices[t] = None
    return prices
