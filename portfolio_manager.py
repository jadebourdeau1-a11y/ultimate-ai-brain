class Portfolio:
    def __init__(self):
        self.assets = {}
        self.history = []

    def update(self, trade):
        t = trade['ticker']
        self.assets[t] = self.assets.get(t, 0) + (1 if trade['action']=="BUY" else -1)
        self.history.append(trade)

    def summary(self):
        return self.assets

    def trade_log(self):
        return self.history
