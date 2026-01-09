def get_portfolio_value(portfolio, current_prices):
    """Calculate total portfolio value."""
    value = portfolio["cash"]
    for ticker, amount in portfolio["positions"].items():
        value += current_prices.get(ticker, 0) * amount
    return round(value, 2)
