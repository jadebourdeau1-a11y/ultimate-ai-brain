from sklearn.linear_model import LinearRegression
import numpy as np

def predict_price(prices):
    """Predict the next price using a simple linear regression."""
    X = np.arange(len(prices)).reshape(-1, 1)
    y = np.array(prices)
    model = LinearRegression()
    model.fit(X, y)
    return round(model.predict(np.array([[len(prices) + 1]]))[0], 2)
