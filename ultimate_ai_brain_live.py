import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from portfolio_manager import portfolio_summary, get_holdings, get_prices
from ml_prediction import get_predictions
import datetime

st.set_page_config(page_title="Ultimate AI Brain Dashboard", layout="wide")

st.title("Ultimate AI Brain LIVE Dashboard")

# --- Fetch portfolio data ---
holdings = get_holdings()  # dict: {'Asset': 'quantity'}
prices = get_prices(list(holdings.keys()))  # dict: {'Asset': price}

# --- Portfolio summary ---
df, total_value = portfolio_summary(prices, holdings)
st.subheader("Portfolio Summary")
st.metric("Total Portfolio Value", f"${total_value:,.2f}")

# --- Portfolio value over time ---
st.subheader("Portfolio Value Over Time")

# Generate historical data for demo (replace with real historical if available)
history_file = "portfolio_history.csv"
try:
    history_df = pd.read_csv(history_file, parse_dates=["Date"])
except FileNotFoundError:
    history_df = pd.DataFrame(columns=["Date", "TotalValue"])
history_df = history_df.append({"Date": datetime.date.today(), "TotalValue": total_value}, ignore_index=True)
history_df.to_csv(history_file, index=False)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(history_df["Date"], history_df["TotalValue"], marker='o', linestyle='-')
ax.set_xlabel("Date")
ax.set_ylabel("Portfolio Value ($)")
ax.set_title("Portfolio Value Over Time")
st.pyplot(fig)

# --- Asset allocation ---
st.subheader("Asset Allocation")
allocation_df = df.copy()
allocation_df["Percentage"] = allocation_df["Value"] / total_value * 100
fig2, ax2 = plt.subplots(figsize=(6, 6))
ax2.pie(allocation_df["Percentage"], labels=allocation_df["Asset"], autopct="%1.1f%%", startangle=90)
ax2.axis('equal')
st.pyplot(fig2)

# --- Live prices ---
st.subheader("Live Prices")
live_prices_df = pd.DataFrame(list(prices.items()), columns=["Asset", "Price"])
st.table(live_prices_df)

# --- ML Predictions / Recommendations ---
st.subheader("ML Predictions / Recommendations")
predictions = get_predictions(list(holdings.keys()))  # dict: {'Asset': 'Buy/Hold/Sell'}
pred_df = pd.DataFrame(list(predictions.items()), columns=["Asset", "Recommendation"])
st.table(pred_df)
