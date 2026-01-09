from datetime import datetime

class PortfolioManager:
    def __init__(self, initial_cash=10000):
        self.cash = initial_cash
        self.positions = {}  # asset -> {"quantity": x, "avg_price": y}
        self.trade_history = []

        # Risk settings
        self.max_allocation_per_asset = 0.3  # max 30% of total portfolio per asset
        self.stop_loss_percent = 0.05  # 5%
        self.take_profit_percent = 0.1  # 10%

    def execute_trade(self, asset, action, price, total_portfolio_value):
        allocation_limit = total_portfolio_value * self.max_allocation_per_asset

        if action == "BUY":
            # Calculate how much to buy without exceeding max allocation
            quantity = allocation_limit / price
            if asset in self.positions:
                # Update average price
                old_qty = self.positions[asset]['quantity']
                old_avg = self.positions[asset]['avg_price']
                new_avg = (old_qty * old_avg + quantity * price) / (old_qty + quantity)
                self.positions[asset]['avg_price'] = new_avg
                self.positions[asset]['quantity'] += quantity
            else:
                self.positions[asset] = {"quantity": quantity, "avg_price": price}

            self.cash -= quantity * price
            self.trade_history.append({"asset": asset, "action": "BUY", "price": price, "timestamp": datetime.now()})
            print(f"[BUY] {asset} x {quantity:.4f} at ${price}")

        elif action == "SELL" and asset in self.positions:
            quantity = self.positions[asset]['quantity']
            self.cash += quantity * price
            self.trade_history.append({"asset": asset, "action": "SELL", "price": price, "timestamp": datetime.now()})
            print(f"[SELL] {asset} x {quantity:.4f} at ${price}")
            del self.positions[asset]

    def check_risk(self, market_prices):
        """
        Automatically triggers stop-loss or take-profit
        """
        to_sell = []
        for asset, pos in self.positions.items():
            current_price = market_prices.get(asset)
            if not current_price:
                continue

            # Stop-loss
            if current_price <= pos['avg_price'] * (1 - self.stop_loss_percent):
                print(f"[STOP-LOSS TRIGGERED] {asset}")
                to_sell.append(asset)
            # Take-profit
            elif current_price >= pos['avg_price'] * (1 + self.take_profit_percent):
                print(f"[TAKE-PROFIT TRIGGERED] {asset}")
                to_sell.append(asset)

        return to_sell

    def get_portfolio_value(self, market_prices):
        value = self.cash
        for asset, pos in self.positions.items():
            current_price = market_prices.get(asset, pos['avg_price'])
            value += pos['quantity'] * current_price
        return value

    def get_portfolio_summary(self, market_prices):
        summary = {"cash": self.cash, "positions": self.positions, "total_value": self.get_portfolio_value(market_prices)}
        return summary
