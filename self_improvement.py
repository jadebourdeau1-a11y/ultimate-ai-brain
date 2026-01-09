import csv
from datetime import datetime
import os

TRADE_LOG_FILE = "trade_log.csv"

# Create file if it doesn't exist
if not os.path.exists(TRADE_LOG_FILE):
    with open(TRADE_LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Time", "Asset", "Action", "Price"])

def log_trade(asset, action, price):
    with open(TRADE_LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), asset, action, price])
