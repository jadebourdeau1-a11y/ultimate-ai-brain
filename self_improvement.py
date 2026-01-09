import csv
from datetime import datetime

def log_trade(ticker, action, quantity, price):
    with open("trade_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), ticker, action, quantity, price])
