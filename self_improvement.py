Step 6: Self-Improvement / Logging

Track every trade, price, prediction, and result for learning.

Save to a CSV for now:

import csv

def log_trade(ticker, action, price):
    with open("trade_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([ticker, action, price])