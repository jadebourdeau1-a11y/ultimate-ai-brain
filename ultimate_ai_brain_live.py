<<<<<<< HEAD
import streamlit as st
from data_gathering_multi import get_live_price
from ml_prediction import predict_price
from decision_making import make_decision
from execution import execute_trade
from self_improvement import log_trade, read_logs
from portfolio_manager import get_portfolio_value

# Set page config
st.set_page_config(page_title="Ultimate AI Brain", layout="wide")

st.title("Ultimate AI Brain LIVE Dashboard")

# -------------------------------
# Sidebar: Manual Controls & Risk Settings
# -------------------------------
st.sidebar.header("Manual Controls / Risk Settings")

manual_buy = st.sidebar.text_input("Manual BUY (asset:quantity, e.g., BTC:0.01)")
manual_sell = st.sidebar.text_input("Manual SELL (asset:quantity, e.g., AAPL:1)")

refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 5, 300, 30)
max_allocation = st.sidebar.slider("Max Allocation per Asset (%)", 10, 100, 50)
stop_loss = st.sidebar.slider("Stop-Loss (%)", 1, 50, 10)
take_profit = st.sidebar.slider("Take-Profit (%)", 1, 50, 20)
risk_threshold = st.sidebar.slider("Decision Threshold (%)", 0.1, 5.0, 0.5)

# -------------------------------
# Live Price & ML Prediction
# -------------------------------
ticker = st.text_input("Ticker", "AAPL")

current_price = get_live_price(ticker)
predicted_price = predict_price([current_price])

st.subheader("Live Prices + Predictions")
st.metric(label=f"{ticker} Current Price", value=current_price)
st.metric(label=f"{ticker} Predicted Price", value=predicted_price)

# -------------------------------
# AI Decision & Manual Trade
# -------------------------------
st.subheader("AI Decision / Manual Execution")

# AI decision
ai_action = make_decision(current_price, predicted_price, threshold=risk_threshold)
st.write(f"AI Decision: {ai_action}")

# Manual trade execution
if st.button("Execute AI Trade"):
    portfolio = execute_trade(ai_action, ticker, current_price)
    log_trade(ticker, ai_action, current_price)
    st.write("Portfolio after AI Trade:", portfolio)

if st.button("Execute Manual BUY") and manual_buy:
    asset, qty = manual_buy.split(":")
    portfolio = execute_trade("BUY", asset.strip(), float(qty.strip()))
    log_trade(asset.strip(), "BUY", float(qty.strip()))
    st.write("Portfolio after Manual BUY:", portfolio)

if st.button("Execute Manual SELL") and manual_sell:
    asset, qty = manual_sell.split(":")
    portfolio = execute_trade("SELL", asset.strip(), float(qty.strip()))
    log_trade(asset.strip(), "SELL", float(qty.strip()))
    st.write("Portfolio after Manual SELL:", portfolio)

# -------------------------------
# Trade History
# -------------------------------
st.subheader("Trade Log (Last 10 Trades)")
logs = read_logs()
if logs:
    for log in logs[-10:]:
        st.write(f"{log[0]} - {log[1]} at ${log[2]}")
else:
    st.write("No trades yet.")

# -------------------------------
# Portfolio Summary
# -------------------------------
st.subheader("Portfolio Summary")
try:
    current_prices = {ticker: current_price for ticker in portfolio.get("positions", {})}
    total_value = get_portfolio_value(portfolio, current_prices)
    st.write(f"Cash: ${portfolio['cash']}")
    st.write(f"Positions: {portfolio['positions']}")
    st.write(f"Total Portfolio Value: ${total_value}")
except Exception:
    st.write("Portfolio is empty.")
=======
# ----------------------------
# Imports
# ----------------------------
import time
import pandas as pd
import random
import streamlit as st
from datetime import datetime

# ----------------------------
# Import all modules (make sure these files are in same folder)
# ----------------------------
from data_gathering_multi import MultiDataGathering
from decision_making import DecisionMaking
from execution import Execution
from self_improvement import SelfImprovement
from ml_prediction import PricePredictor
from portfolio_manager import PortfolioManager

# ----------------------------
# Initialize modules
# ----------------------------
data_module = MultiDataGathering()
decision_module = DecisionMaking()
execution_module = Execution()
self_improve_module = SelfImprovement()
predictor = PricePredictor()
portfolio = PortfolioManager(initial_cash=10000)

# ----------------------------
# Streamlit Setup
# ----------------------------
st.set_page_config(page_title="🧠 Ultimate AI Brain LIVE", layout="wide")
st.title("Ultimate AI Brain LIVE Dashboard")

# Sidebar controls
st.sidebar.header("Manual Controls / Risk Settings")
pause_ai = st.sidebar.checkbox("Pause AI", value=False)
manual_buy = st.sidebar.text_input("Manual BUY (asset:quantity, e.g., BTC:0.01)")
manual_sell = st.sidebar.text_input("Manual SELL (asset:quantity, e.g., AAPL:1)")
refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 5, 300, 30)

portfolio.max_allocation_per_asset = st.sidebar.slider("Max Allocation per Asset (%)", 10, 100, 30) / 100
portfolio.stop_loss_percent = st.sidebar.slider("Stop-Loss (%)", 1, 50, 5) / 100
portfolio.take_profit_percent = st.sidebar.slider("Take-Profit (%)", 1, 50, 10) / 100

placeholder = st.empty()

# ----------------------------
# Price memory
# ----------------------------
price_memory = {
    "crypto": {coin: [] for coin in data_module.crypto_list},
    "stocks": {ticker: [] for ticker in data_module.stock_list}
}

# ----------------------------
# Helper: manual trade
# ----------------------------
def parse_trade(trade_str, action):
    if ":" not in trade_str:
        return
    asset, qty = trade_str.split(":")
    try:
        qty = float(qty)
        price = combined_prices.get(asset, {}).get("usd", 0)
        if price > 0:
            portfolio.execute_trade(asset, action, price, portfolio.get_portfolio_value({**combined_prices, **predictions}))
    except:
        pass

# ----------------------------
# Main Loop
# ----------------------------
while True:
    # ----------------------------
    # Step 1: Data Gathering
    # ----------------------------
    data = data_module.get_data()

    # Update price memory
    for coin, info in data.get('crypto', {}).items():
        price_memory['crypto'][coin].append(info['usd'])
    for ticker, price in data.get('stocks', {}).items():
        price_memory['stocks'][ticker].append(price)

    # ----------------------------
    # Step 2: ML Predictions
    # ----------------------------
    predictions = {}
    for coin, prices in price_memory['crypto'].items():
        predictor.train_model(prices[-20:], coin)
        pred = predictor.predict_next(coin)
        predictions[coin] = round(pred, 2) if pred else None
    for ticker, prices in price_memory['stocks'].items():
        predictor.train_model(prices[-20:], ticker)
        pred = predictor.predict_next(ticker)
        predictions[ticker] = round(pred, 2) if pred else None

    # ----------------------------
    # Step 3: Decision Making
    # ----------------------------
    combined_prices = {}
    for coin, info in data.get('crypto', {}).items():
        combined_prices[coin] = {"usd": info['usd']}
    for ticker, price in data.get('stocks', {}).items():
        combined_prices[ticker] = {"usd": price}

    # Manual trades
    if manual_buy:
        parse_trade(manual_buy, "BUY")
    if manual_sell:
        parse_trade(manual_sell, "SELL")

    if pause_ai:
        st.warning("AI Brain paused. No trades executed.")
        time.sleep(refresh_interval)
        continue

    # AI recommendations
    decision_module.analyze_prices(combined_prices)
    recommendations = decision_module.get_recommendations()

    # Adjust recommendations using ML predictions
    for asset, pred_price in predictions.items():
        if pred_price:
            current_price = combined_prices[asset]['usd']
            if pred_price > current_price * 1.01:
                recommendations[asset]['action'] = "BUY"
            elif pred_price < current_price * 0.99:
                recommendations[asset]['action'] = "SELL"

    # ----------------------------
    # Step 4: Portfolio / Execute Trades
    # ----------------------------
    total_value = portfolio.get_portfolio_value({**combined_prices, **predictions})
    for asset, rec in recommendations.items():
        portfolio.execute_trade(asset, rec['action'], combined_prices[asset]['usd'], total_value)

    # Auto risk management
    to_sell = portfolio.check_risk({**combined_prices, **predictions})
    for asset in to_sell:
        portfolio.execute_trade(asset, "SELL", combined_prices[asset]['usd'], total_value)

    # ----------------------------
    # Step 5: Self-Improvement
    # ----------------------------
    for trade in execution_module.get_trade_log():
        future_price = trade['price'] * (1 + random.uniform(-0.03, 0.03))
        self_improve_module.log_trade_result(trade, future_price)
    performance = self_improve_module.get_performance()

    # ----------------------------
    # Step 6: Dashboard Update
    # ----------------------------
    data_df = pd.DataFrame([
        {"Asset": k, "Price (USD)": v["usd"] if isinstance(v, dict) else v} 
        for k, v in combined_prices.items()
    ])
    rec_df = pd.DataFrame([
        {"Asset": k, **v, "Predicted": predictions.get(k)} 
        for k, v in recommendations.items()
    ])
    perf_df = pd.DataFrame([
        {"Asset": k, **v} for k, v in performance.items()
    ])
    trades_df = pd.DataFrame(execution_module.get_trade_log()[-10:])
    portfolio_summary = pd.DataFrame([{
        "Cash": portfolio.cash,
        "Positions": str(portfolio.positions),
        "Total Value": portfolio.get_portfolio_value({**combined_prices, **predictions})
    }])

    with placeholder.container():
        st.subheader("Live Prices")
        st.dataframe(data_df)

        st.subheader("Recommendations + ML Predictions")
        st.dataframe(rec_df)

        st.subheader("Performance / Strategy")
        st.dataframe(perf_df)

        st.subheader("Trade Log (Last 10)")
        st.dataframe(trades_df)

        st.subheader("Portfolio Summary")
        st.dataframe(portfolio_summary)

    time.sleep(refresh_interval)
>>>>>>> f6b98ce059df2bfbd94c62f494194107f598079f
