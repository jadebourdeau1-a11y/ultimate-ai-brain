import csv

def log_trade(ticker, action, price):
    with open("trade_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([ticker, action, price])
