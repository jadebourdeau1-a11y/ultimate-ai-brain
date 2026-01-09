import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from portfolio_manager import get_holdings, get_prices
from ml_prediction import get_predictions
import datetime
import time

st.set_page_config(page_title="Ultimate AI Brain LIVE Dashboard", layout="wide")

st.title("Ultimate AI Brain LIVE Dashboard 💹")

# --- Refresh interval (seconds)
REFRESH_INTERVAL = 60  # refresh every 60 seconds

# --- Main loop
while True:
    # --- Fetch portfolio data ---
    holdings = get_holdings()  # {'Asset': quantity}
    prices = get_prices(list(holdings.keys()))  # {'Asset': price}
    
    # --- Portfolio summary ---
    df = pd.DataFrame([{"Asset": k, "Quantity": v, "Price": prices[k], "Value": v*prices[k]} for k, v in holdings.items()])
    total_value = df["Value"].sum()
    st.subheader("Portfolio Summary")
    st.metric("Total Portfolio Value", f"${total_value:,.2f}")
    
    # --- Portfolio value over time ---
    st.subheader("Portfolio Value Over Time")
    history_file = "portfolio_history.csv"
    try:
        history_df = pd.read_csv(history_file, parse_dates=["Date"])
    except FileNotFoundError:
        history_df = pd.DataFrame(columns=["Date", "TotalValue"])
    history_df = history_df.append({"Date": datetime.date.today(), "TotalValue": total_value}, ignore_index=True)
    history_df.to_csv(history_file, index=False)
    
    st.line_chart(history_df.set_index("Date")["TotalValue"])
    
    # --- Asset allocation ---
    st.subheader("Asset Allocation")
    df["Percentage"] = df["Value"] / total_value * 100
    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(df["Percentage"], labels=df["Asset"], autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)
    
    # --- Live Prices ---
    st.subheader("Live Prices")
    live_prices_df = pd.DataFrame(list(prices.items()), columns=["Asset", "Price"])
    st.table(live_prices_df)
    
    # --- ML Predictions / Recommendations ---
    st.subheader("ML Predictions / Recommendations")
    predictions = get_predictions(list(holdings.keys()))  # {'Asset': 'Buy/Hold/Sell'}
    pred_df = pd.DataFrame(list(predictions.items()), columns=["Asset", "Recommendation"])
    pred_df["Color"] = pred_df["Recommendation"].map({"Buy": "green", "Hold": "orange", "Sell": "red"})
    st.table(pred_df[["Asset", "Recommendation"]])
    
    # --- Wait & refresh ---
    st.info(f"Refreshing in {REFRESH_INTERVAL} seconds...")
    time.sleep(REFRESH_INTERVAL)
    st.experimental_rerun()
