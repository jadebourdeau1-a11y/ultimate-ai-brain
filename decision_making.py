<<<<<<< HEAD
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
=======
from datetime import datetime

class DecisionMaking:
    def __init__(self):
        self.memory = {}  # keeps track of previous prices
        self.recommendations = {}

    def analyze_prices(self, data):
        self.recommendations = {}
        for coin, info in data.items():
            current_price = info.get("usd")
            previous_price = self.memory.get(coin, current_price)
            change_percent = ((current_price - previous_price) / previous_price) * 100

            # Simple logic: if price dropped > 2% → buy, increased > 2% → sell, else hold
            if change_percent <= -2:
                action = "BUY"
            elif change_percent >= 2:
                action = "SELL"
            else:
                action = "HOLD"

            self.recommendations[coin] = {
                "current_price": current_price,
                "change_percent": round(change_percent, 2),
                "action": action
            }

            # Update memory for next cycle
            self.memory[coin] = current_price

        print(f"[{datetime.now()}] Recommendations updated:")
        for coin, rec in self.recommendations.items():
            print(f"  {coin}: {rec['action']} ({rec['change_percent']}%)")

    def get_recommendations(self):
        return self.recommendations
>>>>>>> f6b98ce059df2bfbd94c62f494194107f598079f
