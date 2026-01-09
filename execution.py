portfolio = {"cash": 10000, "positions": {}}

def execute_trade(action, ticker, price, amount=1):
    """Execute a trade and update portfolio."""
    global portfolio
    if action == "BUY" and portfolio["cash"] >= price*amount:
        portfolio["cash"] -= price*amount
        portfolio["positions"][ticker] = portfolio["positions"].get(ticker, 0) + amount
    elif action == "SELL" and portfolio["positions"].get(ticker, 0) >= amount:
        portfolio["cash"] += price*amount
        portfolio["positions"][ticker] -= amount
    return portfolio
