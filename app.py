import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Beginner Investment Assistant", layout="wide")
st.title("💰 Beginner Investment Assistant")

# ----------------- USER INPUTS -----------------
st.header("Step 1: Tell us about yourself")

monthly_income = st.number_input("Monthly Income ($):", min_value=100, step=100)
monthly_savings = st.number_input("Monthly Savings ($):", min_value=0, step=50)
investment_amount = st.number_input("Amount you want to invest now ($):", min_value=50, step=50)

risk_level = st.selectbox(
    "Your Risk Preference:",
    ["Low Risk (Safe & Stable)", "Medium Risk (Balanced Growth)", "High Risk (Potential High Returns)"]
)

st.header("Step 2: Choose a Stock")
stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, MSFT, TSLA):", value="AAPL").upper()

# ----------------- FETCH STOCK DATA -----------------
st.header("Step 3: Stock Analysis")

try:
    data = yf.download(stock_symbol, period="1y")
    if data.empty:
        st.error("Stock symbol not found. Please enter a valid symbol.")
    else:
        # Flatten MultiIndex columns if present
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        # Calculate moving averages
        data["MA50"] = data["Close"].rolling(50).mean()
        data["MA200"] = data["Close"].rolling(200).mean()

        latest_price = float(data["Close"].iloc[-1])

        # Show key metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"${latest_price:.2f}")
        col2.metric("50-Day Avg", f"${float(data['MA50'].iloc[-1]):.2f}")
        col3.metric("200-Day Avg", f"${float(data['MA200'].iloc[-1]):.2f}")

        # ----------------- TREND INSIGHT -----------------
        st.subheader("📈 Trend Analysis (Plain English)")
        ma50 = float(data["MA50"].iloc[-1])
        ma200 = float(data["MA200"].iloc[-1])

        if latest_price > ma50 and latest_price > ma200:
            st.success("The stock is in an upward trend. Good time to consider buying!")
        elif latest_price < ma50 and latest_price < ma200:
            st.warning("The stock is in a downward trend. Consider caution or waiting.")
        else:
            st.info("The stock is moving sideways. Could go either way.")

        # ----------------- ROI SIMULATION -----------------
        st.subheader("💵 Investment Simulation")
        shares_can_buy = investment_amount / latest_price
        st.write(f"With ${investment_amount}, you can buy approx **{shares_can_buy:.2f} shares** of {stock_symbol}.")

        # Historical ROI estimate: simple 6-month past trend
        six_months_ago = float(data["Close"].iloc[-126])  # approx 126 trading days
        past_roi_percent = ((latest_price - six_months_ago) / six_months_ago) * 100
        st.write(f"If this stock had followed the last 6 months trend, your investment could change by **{past_roi_percent:.2f}%**.")

        # Risk guidance
        st.subheader("🔔 Recommendation for You")
        if risk_level == "Low Risk (Safe & Stable)":
            st.write("Based on your low-risk preference, consider investing smaller amounts in stable stocks or ETFs.")
        elif risk_level == "Medium Risk (Balanced Growth)":
            st.write("Medium risk: You can invest a moderate amount. Diversifying across 2-3 stocks is recommended.")
        else:
            st.write("High risk: You are willing to take risks. You could invest more, but be prepared for potential losses.")

        # ----------------- PLOT -----------------
        st.line_chart(data[["Close", "MA50", "MA200"]].ffill())

except Exception as e:
    st.error(f"Error fetching data: {e}")

st.markdown("---")
st.write("This app is for **educational purposes**. Always do your own research before investing.")