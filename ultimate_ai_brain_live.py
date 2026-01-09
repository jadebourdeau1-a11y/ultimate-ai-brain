import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from portfolio_manager import portfolio_summary, update_portfolio

# --------------------------
# Mock live prices (replace with your API or ML predictions)
prices = {
    "BTC": 30000,
    "ETH": 2000,
    "AAPL": 150,
    "TSLA": 800
}

# --------------------------
# Streamlit caching for portfolio history
if "portfolio_history" not in st.session_state:
    st.session_state.portfolio_history = []

# --------------------------
st.set_page_config(page_title="Ultimate AI Brain LIVE", layout="wide")
st.title("Ultimate AI Brain LIVE Dashboard")

# --------------------------
st.sidebar.header("Manual Controls / Risk Settings")
asset_input = st.sidebar.text_input("Asset (e.g., BTC, AAPL)")
quantity_input = st.sidebar.number_input("Quantity", min_value=0.0, step=0.01)
action_input = st.sidebar.selectbox("Action", ["BUY", "SELL"])

if st.sidebar.button("Execute Trade"):
    if asset_input and quantity_input > 0:
        update_portfolio(asset_input, quantity_input, action_input)
        st.sidebar.success(f"{action_input} executed for {quantity_input} {asset_input}")
    else:
        st.sidebar.warning("Please enter valid asset and quantity.")

# --------------------------
# Portfolio summary table
st.header("Portfolio Summary")
try:
    df, total_value = portfolio_summary(prices)
except Exception as e:
    st.error(f"Error calculating portfolio: {e}")
    df = pd.DataFrame(columns=["Asset", "Quantity", "Value"])
    total_value = 0

st.dataframe(df)
st.metric("Total Portfolio Value", f"${total_value:,.2f}")

# --------------------------
# Record portfolio history for chart
st.session_state.portfolio_history.append({"time": datetime.now(), "total_value": total_value})

history_df = pd.DataFrame(st.session_state.portfolio_history)

# --------------------------
# Portfolio Value Over Time
st.header("Portfolio Value Over Time")
if len(history_df) > 0:
    fig_value = px.line(history_df, x="time", y="total_value",
                        title="Portfolio Total Value Over Time",
                        labels={"time": "Time", "total_value": "Total Value ($)"})
    st.plotly_chart(fig_value, use_container_width=True)

# --------------------------
# Asset Allocation Pie Chart
st.header("Asset Allocation")
if len(df) > 0 and df["Value"].sum() > 0:
    fig_pie = px.pie(df, names="Asset", values="Value", title="Asset Allocation by Value")
    st.plotly_chart(fig_pie, use_container_width=True)

# --------------------------
# Live Prices
st.header("Live Prices")
st.dataframe(pd.DataFrame(prices.items(), columns=["Asset", "Price"]))

# --------------------------
# ML Predictions / Recommendations (placeholder)
st.header("ML Predictions / Recommendations")
st.info("ML Predictions will appear here once implemented.")
