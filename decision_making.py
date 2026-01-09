def recommend_trade(prices):
    # Placeholder: Always recommend HOLD
    recommendations = {}
    for asset in prices.columns:
        if asset != "Time":
            recommendations[asset] = "HOLD"
    return recommendations
