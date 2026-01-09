def make_decision(prediction, current_price, stop_loss, take_profit):
    """
    prediction: float (expected return)
    current_price: float
    stop_loss/take_profit: percentages
    """
    action = "HOLD"
    if prediction > 0.02:  # predicted >2% gain
        action = "BUY"
    elif prediction < -0.02:  # predicted >2% loss
        action = "SELL"
    return action
