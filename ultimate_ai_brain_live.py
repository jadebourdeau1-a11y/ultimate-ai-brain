import streamlit as st
from data_gathering_multi import get_prices
from ml_prediction import predict_prices
from decision_making import make_decision
from execution import execute_trade
from portfolio_manager import Portfolio
from self_improvement import log_trade

st.set_page_config(page_title="Ultimate AI Brain", layout="wide")
st.title("Ultimate AI Brain LIVE Dashboard")

# --- Portfolio ---
portfolio = Portfolio()

# --- Manual Controls ---
st.sidebar.header("Manual Controls / Risk Settings")
manual_buy = st.sidebar.text_input("Manual BUY (asset:quantity, e.g., BTC:0.01)")
manual_sell = st.sidebar.text_input("Manual SELL (asset:quantity, e.g., AAPL:1)")
refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 5, 300, 60)
max_allocation = st.sidebar.slider("Max Allocation per Asset (%)", 10, 100, 50)
stop_loss = st.sidebar.slider("Stop-Loss (%)", 1, 50, 10)
take_profit = st.sidebar.slider("Take-Profit (%)", 1, 50, 20)

# --- Fetch Prices ---
prices = get_prices()

# --- AI Predictions ---
predictions = predict_prices(prices)

# --- AI Decisions ---
decisions = make_decision(prices, predictions, max_allocation, stop_loss, take_profit)

# --- Execute Trades ---
for trade in decisions:
    execute_trade(trade)
    log_trade(trade['ticker'], trade['action'], trade['price'])
    portfolio.update(trade)

# --- Display Data ---
st.subheader("Live Prices")
st.write(prices)

st.subheader("Recommendations + ML Predictions")
st.write(predictions)

st.subheader("Portfolio Summary")
st.write(portfolio.summary())

st.subheader("Trade Log (Last 10)")
st.write(portfolio.trade_log()[-10:])
