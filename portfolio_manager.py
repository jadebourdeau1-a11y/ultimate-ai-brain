import pandas as pd

portfolio = {}

def update_portfolio(ticker, action, quantity, price):
    global portfolio
    if ticker not in portfolio:
        portfolio[ticker] = {"quantity": 0, "avg_price": 0}
    if action == "BUY":
        total_cost = portfolio[ticker]["avg_price"] * portfolio[ticker]["quantity"] + price * quantity
        portfolio[ticker]["quantity"] += quantity
        portfolio[ticker]["avg_price"] = total_cost / portfolio[ticker]["quantity"]
    elif action == "SELL":
        portfolio[ticker]["quantity"] -= quantity
        if portfolio[ticker]["quantity"] <= 0:
            portfolio[ticker]["quantity"] = 0
            portfolio[ticker]["avg_price"] = 0

def portfolio_summary(current_prices):
    summary = []
    total_value = 0
    for t, data in portfolio.items():
        qty = data["quantity"]
        if qty == 0: continue
        price = current_prices.get(t, 0)
        value = qty * price
        profit = (price - data["avg_price"]) * qty
        total_value += value
        summary.append({
            "Ticker": t,
            "Quantity": qty,
            "Avg Price": data["avg_price"],
            "Current Price": price,
            "Value": value,
            "Profit": profit
        })
    df = pd.DataFrame(summary)
    df["Value"] = df["Value"].round(2)
    df["Profit"] = df["Profit"].round(2)
    return df, total_value
