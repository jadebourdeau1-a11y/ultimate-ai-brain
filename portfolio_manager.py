import pandas as pd

# Example portfolio, replace with your dynamic portfolio if needed
portfolio = {
    "BTC": 0.1,
    "ETH": 1.5,
    "AAPL": 2,
    "TSLA": 1
}

def portfolio_summary(prices):
    """
    Returns a DataFrame with portfolio summary and total value.
    Prices is a dict like {"BTC": 30000, "ETH": 2000, "AAPL": 150}
    """
    # Create DataFrame from portfolio
    df = pd.DataFrame(list(portfolio.items()), columns=["Asset", "Quantity"])

    # Calculate value safely
    df["Value"] = df.apply(lambda row: row["Quantity"] * prices.get(row["Asset"], 0), axis=1)

    # Round the Value column
    df["Value"] = df["Value"].round(2)

    # Total portfolio value
    total_value = df["Value"].sum()

    return df, total_value

def update_portfolio(asset, quantity, action="BUY"):
    """
    Updates portfolio dictionary.
    """
    if action.upper() == "BUY":
        portfolio[asset] = portfolio.get(asset, 0) + quantity
    elif action.upper() == "SELL":
        portfolio[asset] = max(portfolio.get(asset, 0) - quantity, 0)
    return portfolio
