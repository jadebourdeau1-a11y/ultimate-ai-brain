import yfinance as yf

def get_prices():
    tickers = ["AAPL", "TSLA", "BTC-USD"]
    prices = {}
    for t in tickers:
        prices[t] = yf.Ticker(t).history(period="1d")["Close"].iloc[-1]
    return prices
