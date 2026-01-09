from datetime import datetime

class Execution:
    def __init__(self):
        # This would normally include API keys
        self.sandbox_mode = True  # True = test environment, False = live trading
        self.actions_log = []

    def execute_trade(self, recommendations):
        for coin, rec in recommendations.items():
            action = rec['action']
            price = rec['current_price']

            # Skip HOLD actions
            if action == "HOLD":
                continue

            trade_info = {
                "coin": coin,
                "action": action,
                "price": price,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "SIMULATED" if self.sandbox_mode else "EXECUTED"
            }

            # Here you would integrate with a real API (e.g., Binance, Coinbase)
            # For sandbox/testing, we just log the trade
            self.actions_log.append(trade_info)
            print(f"[{trade_info['timestamp']}] {action} {coin} at ${price} ({trade_info['status']})")

    def get_trade_log(self):
        return self.actions_log
