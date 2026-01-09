import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
from data_gathering_multi import get_prices
from decision_making import recommend_trade
from execution import execute_trade
from self_improvement import log_trade
from ml_prediction import predict_price
from portfolio_manager import get_portfolio_metrics

# Sidebar controls
st.sidebar.header("Manual Controls / Risk Settings")
manual_buy = st.sidebar.text_input("Manual BUY (asset:qty, e.g., BTC:0.01)")
manual_sell = st.sidebar.text_input("Manual SELL (asset:qty, e.g., AAPL:1)")
refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 5, 300, 60)
max_alloc = st.sidebar.slider("Max Allocation per Asset (%)", 10, 100, 50)
stop_loss = st.sidebar.slider("Stop-Loss (%)", 1, 50, 10)
take_profit = st.sidebar.slider("Take-Profit (%)", 1, 50, 10)

st.title("Ultimate AI Brain LIVE Dashboard")

# Get live prices
price_data = get_prices()

# Display price chart
st.subheader("Live Prices")
df_melted = price_data.melt('Time', var_name='Asset', value_name='Price')
chart = alt.Chart(df_melted).mark_line(point=True).encode(
    x='Time',
    y='Price',
    color='Asset'
).interactive()
st.altair_chart(chart, use_container_width=True)

# Portfolio metrics
st.subheader("Portfolio Metrics")
metrics = get_portfolio_metrics()
col1, col2, col3 = st.columns(3)
col1.metric("Portfolio Value", f"${metrics['value']}")
col2.metric("Daily P/L", f"${metrics['daily_pnl']}")
col3.metric("Total Trades", metrics['total_trades'])

# Trade log
st.subheader("Trade Log (Last 10)")
trade_log = pd.read_csv("trade_log.csv")
st.dataframe(trade_log.tail(10))

# Performance chart
st.subheader("Portfolio Performance")
st.line_chart(pd.DataFrame(metrics['performance']).set_index('Time'))

# Manual actions
if manual_buy:
    try:
        asset, qty = manual_buy.split(":")
        price = price_data[asset.strip()].iloc[-1]
        execute_trade(asset.strip(), "BUY", float(qty.strip()), price)
        log_trade(asset.strip(), "BUY", price)
        st.success(f"Executed BUY {qty.strip()} of {asset.strip()} at ${price}")
    except Exception as e:
        st.error(f"Failed BUY: {e}")

if manual_sell:
    try:
        asset, qty = manual_sell.split(":")
        price = price_data[asset.strip()].iloc[-1]
        execute_trade(asset.strip(), "SELL", float(qty.strip()), price)
        log_trade(asset.strip(), "SELL", price)
        st.success(f"Executed SELL {qty.strip()} of {asset.strip()} at ${price}")
    except Exception as e:
        st.error(f"Failed SELL: {e}")

st.caption(f"Dashboard last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
