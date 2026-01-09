<<<<<<< HEAD
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_price(prices):
    """Predict the next price using a simple linear regression."""
    X = np.arange(len(prices)).reshape(-1, 1)
    y = np.array(prices)
    model = LinearRegression()
    model.fit(X, y)
    return round(model.predict(np.array([[len(prices) + 1]]))[0], 2)
=======
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
>>>>>>> f6b98ce059df2bfbd94c62f494194107f598079f
