import streamlit as st
import pandas as pd
import plotly.express as px
from data_gathering_multi import get_portfolio_prices
from ml_prediction import predict_price_change
from decision_making import make_decision
from execution import execute_trade
from portfolio_manager import update_portfolio, portfolio_summary

st.set_page_config(page_title="Ultimate AI Brain", layout="wide")

st.title("Ultimate AI Brain LIVE Dashboard")

# --- Manual Controls ---
st.sidebar.header("Manual Controls / Risk Settings")
manual_buy = st.sidebar.text_input("Manual BUY (asset:quantity, e.g., BTC:0.01)")
manual_sell = st.sidebar.text_input("Manual SELL (asset:quantity, e.g., AAPL:1)")
refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 5, 300, 30)
max_alloc = st.sidebar.slider("Max Allocation per Asset (%)", 10, 100, 50)
stop_loss = st.sidebar.slider("Stop-Loss (%)", 1, 50, 5)
take_profit = st.sidebar.slider("Take-Profit (%)", 1, 50, 10)

# --- Asset list ---
tickers = ["AAPL", "GOOG", "TSLA", "BTC-USD", "ETH-USD"]

# --- Fetch prices ---
prices = get_portfolio_prices(tickers)

# --- ML Predictions ---
predictions = {t: predict_price_change(t) for t in tickers}

# --- Recommendations ---
recommendations = {t: make_decision(predictions[t], prices[t], stop_loss, take_profit) for t in tickers}

# --- Display Prices & Recommendations ---
st.subheader("Live Prices & ML Recommendations")
price_df = pd.DataFrame({
    "Ticker": tickers,
    "Current Price": [prices[t] for t in tickers],
    "Prediction": [predictions[t] for t in tickers],
    "Recommendation": [recommendations[t] for t in tickers]
})
st.dataframe(price_df)

# --- Execute Manual Trades ---
if manual_buy:
    try:
        t, q = manual_buy.split(":")
        execute_trade(t, "BUY", float(q), prices[t])
        update_portfolio(t, "BUY", float(q), prices[t])
    except:
        st.error("Invalid manual buy input")
if manual_sell:
    try:
        t, q = manual_sell.split(":")
        execute_trade(t, "SELL", float(q), prices[t])
        update_portfolio(t, "SELL", float(q), prices[t])
    except:
        st.error("Invalid manual sell input")

# --- Portfolio Summary ---
st.subheader("Portfolio Summary")
df, total_value = portfolio_summary(prices)
st.write(f"Total Portfolio Value: ${total_value:.2f}")
st.dataframe(df)

# --- Charts ---
st.subheader("Portfolio Distribution")
fig = px.pie(df, names="Ticker", values="Value", title="Portfolio Allocation")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Trade Predictions vs Recommendations")
fig2 = px.bar(price_df, x="Ticker", y="Prediction", color="Recommendation", title="ML Predictions")
st.plotly_chart(fig2, use_container_width=True)
