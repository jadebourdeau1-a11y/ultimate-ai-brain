from datetime import datetime

class SelfImprovement:
    def __init__(self):
        # Keeps track of trade performance
        self.trade_history = []  # Each entry: {coin, action, price, outcome}
        self.performance_memory = {}  # e.g., coin -> success rate

    def log_trade_result(self, trade, market_price_after):
        """
        trade: dict from Execution module
        market_price_after: price at a fixed interval after trade (e.g., 10 min)
        """
        action = trade['action']
        buy_price = trade['price']
        coin = trade['coin']

        # Simple evaluation logic
        if action == "BUY":
            profit = market_price_after - buy_price
        elif action == "SELL":
            profit = buy_price - market_price_after
        else:
            profit = 0

        outcome = "PROFIT" if profit > 0 else "LOSS" if profit < 0 else "BREAKEVEN"

        self.trade_history.append({
            "coin": coin,
            "action": action,
            "buy_price": buy_price,
            "market_price_after": market_price_after,
            "profit": round(profit, 2),
            "outcome": outcome,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # Update performance memory
        stats = self.performance_memory.get(coin, {"trades": 0, "wins": 0})
        stats['trades'] += 1
        if profit > 0:
            stats['wins'] += 1
        stats['win_rate'] = round(stats['wins'] / stats['trades'] * 100, 2)
        self.performance_memory[coin] = stats

        print(f"[{datetime.now()}] Trade result logged: {coin} {action} → {outcome}, Profit: ${profit}")

    def get_performance(self):
        return self.performance_memory

    def review_strategy(self):
        """
        Example: adjust thresholds or confidence based on performance
        """
        for coin, stats in self.performance_memory.items():
            if stats['win_rate'] < 50:
                print(f"Warning: {coin} strategy underperforming ({stats['win_rate']}% wins)")
                # Example action: future decisions could be more conservative
            else:
                print(f"{coin} strategy looks strong ({stats['win_rate']}% wins)")
