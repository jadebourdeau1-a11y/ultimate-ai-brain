import yfinance as yf

def get_live_price(ticker="AAPL"):
    """Fetch the latest price of a ticker."""
    data = yf.download(tickers=ticker, period="1d", interval="1m")
    return round(data['Close'].iloc[-1], 2)
