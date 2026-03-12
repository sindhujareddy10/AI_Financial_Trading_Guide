import streamlit as st
import yfinance as yf
import pandas as pd

# -------------------------------
# Session State
# -------------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"

# -------------------------------
# Beginner Financial Dictionary
# -------------------------------

financial_terms = {
    "ROI": "Return on Investment. It shows how much profit or loss you make from your investment.",
    "Moving Average": "The average stock price over a certain number of days. It helps identify the stock trend.",
    "Volatility": "How much the stock price moves up and down. High volatility means higher risk.",
    "Trend": "The general direction of the stock price (going up, down, or sideways).",
    "Diversification": "Investing in multiple stocks instead of one to reduce risk."
}

def tooltip(term):
    explanation = financial_terms.get(term, "")
    return f"""
    <span title="{explanation}" style="
        border-bottom:1px dotted gray;
        cursor:help;
        font-weight:600;">
        {term}
    </span>
    """

# -------------------------------
# Page Config
# -------------------------------

st.set_page_config(page_title="Beginner Investment Assistant", layout="wide")

# -------------------------------
# Top Navigation
# -------------------------------

title_col, btn1, btn2 = st.columns([6,1,1])

with title_col:
    st.title("💰 Beginner Investment Assistant")

with btn1:
    if st.button("📊 Compare"):
        st.session_state.page = "compare"

with btn2:
    if st.button("📚 Terms"):
        st.session_state.page = "terms"

# =====================================================
# MAIN PAGE
# =====================================================

if st.session_state.page == "home":

    st.header("Step 1: Tell us about yourself")

    monthly_income = st.number_input("Monthly Income ($)", min_value=100, step=100)
    monthly_savings = st.number_input("Monthly Savings ($)", min_value=0, step=50)
    investment_amount = st.number_input("Amount you want to invest now ($)", min_value=50, step=50)

    if investment_amount > monthly_savings:
        st.warning(
            "⚠️ You are investing more than your monthly savings. "
            "Make sure you keep emergency funds before investing."
        )

    risk_level = st.selectbox(
        "Your Risk Preference",
        [
            "Low Risk (Safe & Stable)",
            "Medium Risk (Balanced Growth)",
            "High Risk (Potential High Returns)"
        ]
    )

    # -------------------------------------------------
    # NEW FEATURE: Automatic Company Recommendation
    # -------------------------------------------------

    st.header("🤖 Best Company Based on Your Investment")

    if st.button("Find Best Stock To Invest"):

        companies = ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL"]

        best_stock = None
        best_return = -999

        for company in companies:

            ticker = yf.Ticker(company)
            data = ticker.history(period="6mo")

            if not data.empty:

                current_price = data["Close"].iloc[-1]
                past_price = data["Close"].iloc[0]

                return_pct = ((current_price - past_price) / past_price) * 100

                # Check if user can afford at least 1 share
                if investment_amount >= current_price:

                    if return_pct > best_return:
                        best_return = return_pct
                        best_stock = company
                        best_price = current_price

        if best_stock:

            shares = investment_amount / best_price

            st.success(
                f"✅ Recommended Company: **{best_stock}**\n\n"
                f"Current Price: ${best_price:.2f}\n\n"
                f"With ${investment_amount} you can buy **{shares:.2f} shares**.\n\n"
                f"Recent Growth Potential: **{best_return:.2f}%**"
            )

        else:

            st.error(
                "❌ Your investment amount is too low to buy these stocks."
            )

    # -------------------------------------------------

    st.header("Step 2: Choose a Stock")

    stock_symbol = st.text_input(
        "Enter Stock Symbol (e.g., AAPL, MSFT, TSLA)",
        value="AAPL"
    ).upper()

    st.header("Step 3: Stock Analysis")

    try:

        ticker = yf.Ticker(stock_symbol)
        data = ticker.history(period="1y")

        if data.empty:
            st.error("Unable to fetch stock data. Please check the stock symbol.")

        else:

            data["MA50"] = data["Close"].rolling(50).mean()
            data["MA200"] = data["Close"].rolling(200).mean()

            latest_price = float(data["Close"].iloc[-1])

            col1, col2, col3 = st.columns(3)

            col1.metric("Current Price", f"${latest_price:.2f}")

            col2.metric(
                "50-Day Moving Average",
                f"${data['MA50'].iloc[-1]:.2f}",
                help=financial_terms["Moving Average"]
            )

            col3.metric(
                "200-Day Moving Average",
                f"${data['MA200'].iloc[-1]:.2f}",
                help=financial_terms["Moving Average"]
            )

            st.markdown("### 📈 Trend Analysis")

            ma50 = float(data["MA50"].iloc[-1])
            ma200 = float(data["MA200"].iloc[-1])

            if latest_price > ma50 and latest_price > ma200:
                st.success("The stock appears to be trending upward.")

            elif latest_price < ma50 and latest_price < ma200:
                st.warning("The stock appears to be trending downward.")

            else:
                st.info("The stock is moving sideways.")

            st.markdown("### 💵 Investment Simulation")

            shares = investment_amount / latest_price

            st.info(
                f"With ${investment_amount}, you could buy about **{shares:.2f} shares** "
                f"of {stock_symbol}."
            )

            if len(data) > 126:
                past_price = float(data["Close"].iloc[-126])
                roi = ((latest_price - past_price) / past_price) * 100

                st.success(
                    f"If the stock performs similar to the past 6 months, "
                    f"your investment could change by **{roi:.2f}% ROI**."
                )

            st.subheader("📊 Stock Price Trend")

            st.line_chart(data[["Close", "MA50", "MA200"]])

            # Buy Sell Indicator
            st.subheader("💡 Current Recommendation")

            if latest_price > ma50 and latest_price > ma200:
                st.success("📈 Recommendation: BUY")

            elif latest_price < ma50 and latest_price < ma200:
                st.error("📉 Recommendation: SELL / AVOID")

            else:
                st.info("⚖ Recommendation: HOLD / WAIT")

    except Exception as e:
        st.error(f"Error fetching stock data: {e}")

# =====================================================
# STOCK COMPARISON PAGE
# =====================================================

elif st.session_state.page == "compare":

    st.header("📊 Compare Stocks")

    if st.button("⬅ Home"):
        st.session_state.page = "home"

    stock1 = st.text_input("Stock 1", "AAPL")
    stock2 = st.text_input("Stock 2", "MSFT")
    stock3 = st.text_input("Stock 3", "TSLA")

    if st.button("Run Comparison"):

        stocks = [stock1.upper(), stock2.upper(), stock3.upper()]
        results = {}

        for s in stocks:

            ticker = yf.Ticker(s)
            data = ticker.history(period="1y")

            if not data.empty:

                current = data["Close"].iloc[-1]
                past = data["Close"].iloc[0]

                return_pct = ((current - past) / past) * 100
                volatility = data["Close"].pct_change().std() * 100

                results[s] = {
                    "Profit Potential (%)": round(return_pct,2),
                    "Risk Level (%)": round(volatility,2)
                }

        df = pd.DataFrame(results).T
        st.dataframe(df)

        chart_data = pd.DataFrame()

        for s in stocks:
            ticker = yf.Ticker(s)
            data = ticker.history(period="6mo")
            chart_data[s] = data["Close"]

        st.line_chart(chart_data)

# =====================================================
# TERMS PAGE
# =====================================================

elif st.session_state.page == "terms":

    st.header("📚 Beginner Financial Terms")

    if st.button("⬅ Home"):
        st.session_state.page = "home"

    for term, explanation in financial_terms.items():
        st.markdown(f"**{term}**")
        st.caption(explanation)

# -------------------------------
# Disclaimer
# -------------------------------

st.markdown("---")
st.write(
    "This app is for **educational purposes only**. Always research before investing."
)
