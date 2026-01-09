from sklearn.linear_model import LinearRegression
import numpy as np

class PricePredictor:
    def __init__(self):
        self.models = {}  # one model per asset

    def train_model(self, prices, asset_name):
        """
        prices: list of past prices (ordered oldest -> newest)
        """
        if len(prices) < 5:
            return None  # not enough data

        X = np.arange(len(prices)).reshape(-1, 1)  # time steps
        y = np.array(prices)
        model = LinearRegression()
        model.fit(X, y)
        self.models[asset_name] = model

    def predict_next(self, asset_name):
        model = self.models.get(asset_name)
        if not model:
            return None
        next_time = np.array([[len(model.coef_)]])  # predict next step
        return float(model.predict([[len(model.coef_)]])[0])
