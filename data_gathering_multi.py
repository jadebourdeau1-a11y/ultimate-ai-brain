import requests
import yfinance as yf
from datetime import datetime

class MultiDataGathering:
    def __init__(self):
        self.crypto_list = ["bitcoin", "ethereum", "dogecoin"]
        self.stock_list = ["AAPL", "TSLA", "AMZN"]
        self.data = {}

    def fetch_crypto_prices(self):
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": ",".join(self.crypto_list),
            "vs_currencies": "usd"
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                self.data['crypto'] = response.json()
            else:
                print(f"Crypto fetch failed: {response.status_code}")
        except Exception as e:
            print(f"Crypto fetch error: {e}")

    def fetch_stock_prices(self):
        self.data['stocks'] = {}
        try:
            for ticker in self.stock_list:
                stock = yf.Ticker(ticker)
                price = stock.history(period="1d")['Close'][-1]
                self.data['stocks'][ticker] = round(price, 2)
        except Exception as e:
            print(f"Stock fetch error: {e}")

    def get_data(self):
        self.fetch_crypto_prices()
        self.fetch_stock_prices()
        return self.data
