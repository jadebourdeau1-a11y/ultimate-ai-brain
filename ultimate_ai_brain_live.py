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
