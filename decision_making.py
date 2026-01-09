def make_decision(prices, predictions, max_alloc, stop_loss, take_profit):
    decisions = []
    for t in prices:
        if predictions[t] > prices[t]:
            decisions.append({"ticker": t, "action": "BUY", "price": prices[t]})
        else:
            decisions.append({"ticker": t, "action": "SELL", "price": prices[t]})
    return decisions
