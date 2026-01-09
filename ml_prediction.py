import random

def predict_price_change(ticker):
    """
    Simulate an ML prediction for the next price move.
    Returns float between -0.05 and 0.05 (loss/gain %)
    """
    return round(random.uniform(-0.05, 0.05), 4)
