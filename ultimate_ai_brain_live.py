import streamlit as st
import pandas as pd
from data_gathering_multi import MultiDataGathering
from decision_making import DecisionMaking
from execution import Execution
from self_improvement import SelfImprovement
from ml_prediction import PricePredictor
from portfolio_manager import PortfolioManager
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every 10 seconds (10000 ms)
st_autorefresh(interval=10000, limit=None, key="datarefresh")

# Initialize modules
data_module = MultiDataGathering()
decision_module = DecisionMaking()
execution_module = Execution()
self_improve_module = SelfImprovement()
predictor = PricePredictor()
portfolio = PortfolioManager(initial_cash=10000)

# Streamlit UI
st.set_page_config(page_title="Ultimate AI Brain LIVE", layout="wide")
st.title("Ultimate AI Brain LIVE Dashboard")

# Sidebar controls
st.sidebar.header("Controls")
pause_ai = st.sidebar.checkbox("Pause AI", False)
manual_buy = st.sidebar.text_input("Manual BUY (asset:qty)")
manual_sell = st.sidebar.text_input("Manual SELL (asset:qty)")

portfolio.max_allocation_per_asset = st.sidebar.slider(
    "Max Allocation per Asset (%)", 10, 100, 30
) / 100
portfolio.stop_loss_percent = st.sidebar.slider("Stop-Loss (%)", 1, 50, 5) / 100
portfolio.take_profit_percent = st.sidebar.slider("Take-Profit (%)", 1, 50, 10) / 100

# Fetch data
data = data_module.get_data()
predictions = predictor.predict(data)
recommendations = decision_module.get_recommendations(data, predictions)

# Handle manual trades
if manual_buy:
    try:
        asset, qty = manual_buy.split(":")
        portfolio.execute_trade(asset.strip(), "buy", data.get(asset.strip(), 0), int(qty))
    except:
        st.sidebar.error("Manual BUY format invalid. Use asset:qty")
if manual_sell:
    try:
        asset, qty = manual_sell.split(":")
        portfolio.execute_trade(asset.strip(), "sell", data.get(asset.strip(), 0), int(qty))
    except:
        st.sidebar.error("Manual SELL format invalid. Use asset:qty")

# Execute AI recommendations only if not paused
if not pause_ai:
    for asset, rec in recommendations.items():
        portfolio.execute_trade(asset, rec["action"], rec["price"], portfolio.get_portfolio_value())

# Prepare dashboard display
summary = {
    "Cash": portfolio.cash,
    "Positions": portfolio.positions,
    "Total Value": portfolio.get_portfolio_value()
}
st.subheader("Portfolio Summary")
st.dataframe(pd.DataFrame([summary]))

st.subheader("Portfolio Value Over Time")
st.line_chart(portfolio.value_history)

st.subheader("Asset Allocation")
st.bar_chart(portfolio.get_allocation())

st.subheader("Live Prices")
st.dataframe(pd.DataFrame(data, index=[0]))

st.subheader("ML Predictions / Recommendations")
st.dataframe(pd.DataFrame(recommendations).T)
