def make_decision(current_price, predicted_price, threshold=0.5):
    """
    Decide whether to BUY, SELL, or HOLD based on predicted price.
    Threshold is a percentage for sensitivity.
    """
    if predicted_price > current_price * (1 + threshold/100):
        return "BUY"
    elif predicted_price < current_price * (1 - threshold/100):
        return "SELL"
    else:
        return "HOLD"
