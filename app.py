import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# ------------------------------------------------
# Page Config
# ------------------------------------------------

st.set_page_config(
    page_title="AI Beginner Investment Assistant",
    page_icon="📈",
    layout="wide"
)

# ------------------------------------------------
# Session State
# ------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"

if "risk_level" not in st.session_state:
    st.session_state.risk_level = "Medium Risk"

# ------------------------------------------------
# Financial Terms
# ------------------------------------------------

financial_terms = {
    "ROI": "Return on Investment – profit percentage from an investment.",
    "Moving Average": "Average stock price used to identify trends.",
    "Volatility": "How much stock prices fluctuate.",
    "Trend": "General direction of stock price movement."
}

# ------------------------------------------------
# Navigation
# ------------------------------------------------

col1,col2,col3 = st.columns([6,1,1])

with col1:
    st.title("📈 AI Beginner Investment Assistant")

with col2:
    if st.button("📊 Compare"):
        st.session_state.page = "compare"

with col3:
    if st.button("📚 Terms"):
        st.session_state.page = "terms"

# =================================================
# HOME PAGE
# =================================================

if st.session_state.page == "home":

    st.header("💰 Financial Information")

    monthly_income = st.number_input("Monthly Income ($)",100)
    monthly_savings = st.number_input("Monthly Savings ($)",0)
    investment_amount = st.number_input("Investment Amount ($)",50)

    if investment_amount > monthly_savings:
        st.warning("⚠ Investing more than savings can be risky.")

    st.session_state.risk_level = st.selectbox(
        "Risk Preference",
        ["Low Risk","Medium Risk","High Risk"]
    )

# ------------------------------------------------
# Best Stock Recommendation
# ------------------------------------------------

    st.header("🤖 Best Stock Recommendation")

    if st.button("Find Best Stock"):

        companies = ["AAPL","MSFT","TSLA","AMZN","GOOGL"]

        best_stock = None
        best_return = -999

        for c in companies:

            ticker = yf.Ticker(c)
            data = ticker.history(period="6mo")

            if not data.empty:

                current = data["Close"].iloc[-1]
                past = data["Close"].iloc[0]

                return_pct = ((current-past)/past)*100

                if investment_amount >= current:

                    if return_pct > best_return:
                        best_return = return_pct
                        best_stock = c
                        best_price = current

        if best_stock:

            shares = investment_amount/best_price

            st.success(f"""
Recommended Stock: **{best_stock}**

Price: ${best_price:.2f}

Shares You Can Buy: **{shares:.2f}**

6 Month Growth: **{best_return:.2f}%**
""")

# ------------------------------------------------
# Stock Analysis
# ------------------------------------------------

    st.header("📊 Stock Analysis")

    symbol = st.text_input("Enter Stock Symbol","AAPL").upper()

    try:

        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1y")

        if data.empty:
            st.error("Invalid stock symbol.")

        else:

            data["MA50"] = data["Close"].rolling(50).mean()
            data["MA200"] = data["Close"].rolling(200).mean()

            price = data["Close"].iloc[-1]
            ma50 = data["MA50"].iloc[-1]
            ma200 = data["MA200"].iloc[-1]

            c1,c2,c3 = st.columns(3)

            c1.metric("Current Price",f"${price:.2f}")

            c2.metric(
                "50 Day Moving Average",
                f"${ma50:.2f}",
                help=financial_terms["Moving Average"]
            )

            c3.metric(
                "200 Day Moving Average",
                f"${ma200:.2f}",
                help=financial_terms["Moving Average"]
            )

# ------------------------------------------------
# Trend Analysis
# ------------------------------------------------

            st.subheader("Trend Analysis")

            if price > ma50 and price > ma200:
                st.success("📈 Uptrend")

            elif price < ma50 and price < ma200:
                st.error("📉 Downtrend")

            else:
                st.info("⚖ Sideways Trend")

# ------------------------------------------------
# Investment Simulation
# ------------------------------------------------

            shares = investment_amount/price
            st.info(f"You can buy **{shares:.2f} shares** of {symbol}.")

# ------------------------------------------------
# Interactive Chart
# ------------------------------------------------

            st.subheader("📉 Interactive Stock Chart")

            fig = px.line(
                data,
                y=["Close","MA50","MA200"],
                title=f"{symbol} Stock Trend"
            )

            st.plotly_chart(fig,use_container_width=True)

# ------------------------------------------------
# Chart Explanation
# ------------------------------------------------

            with st.expander("📖 Understanding This Stock Chart"):

                st.write("""
This chart shows the stock's **historical price movement**.

Close Price → actual stock price.

50 Day Moving Average → short-term trend.

200 Day Moving Average → long-term trend.

If price stays above both averages → strong bullish trend.
""")

# ------------------------------------------------
# Final Recommendation
# ------------------------------------------------

            st.subheader("🤖 Final Investment Recommendation")

            reasons = []

            if investment_amount > monthly_savings:
                reasons.append("Investment exceeds monthly savings.")

            risk = st.session_state.risk_level

            if risk == "Low Risk":

                if price > ma200:
                    decision = "BUY (Stable Long Term Trend)"
                else:
                    decision = "HOLD / WAIT"
                    reasons.append("Trend not strong enough for low risk.")

            elif risk == "Medium Risk":

                if price > ma50:
                    decision = "BUY (Moderate Growth Opportunity)"
                else:
                    decision = "HOLD"
                    reasons.append("Short term trend is weak.")

            else:

                if price > ma50 or price > ma200:
                    decision = "BUY (High Risk High Reward)"
                else:
                    decision = "SPECULATIVE / WAIT"
                    reasons.append("Trend weak even for high risk.")

            st.success(f"Recommendation: **{decision}**")

            if reasons:
                st.info("Considerations:\n\n- " + "\n- ".join(reasons))

    except Exception as e:
        st.error(f"Error: {e}")

# =================================================
# COMPARE PAGE
# =================================================

elif st.session_state.page == "compare":

    st.header("📊 Stock Comparison")

    if st.button("⬅ Home"):
        st.session_state.page="home"

    s1 = st.text_input("Stock 1","AAPL")
    s2 = st.text_input("Stock 2","MSFT")
    s3 = st.text_input("Stock 3","TSLA")

    if st.button("Compare Stocks"):

        stocks=[s1.upper(),s2.upper(),s3.upper()]
        results={}

        for s in stocks:

            ticker=yf.Ticker(s)
            data=ticker.history(period="1y")

            if not data.empty:

                current=data["Close"].iloc[-1]
                past=data["Close"].iloc[0]

                return_pct=((current-past)/past)*100
                vol=data["Close"].pct_change().std()*100

                results[s]={
                    "Profit Potential":round(return_pct,2),
                    "Risk":round(vol,2)
                }

        df=pd.DataFrame(results).T
        st.dataframe(df)

        chart=pd.DataFrame()

        for s in stocks:
            ticker=yf.Ticker(s)
            data=ticker.history(period="6mo")
            chart[s]=data["Close"]

        fig=px.line(chart,title="Stock Performance Comparison")
        st.plotly_chart(fig,use_container_width=True)

        with st.expander("📖 How to Read This Graph"):

            st.write("""
Each line represents a stock.

Upward line → good growth.

Flat line → stable.

Highly fluctuating line → higher volatility.
""")

        risk=st.session_state.risk_level

        if risk=="Low Risk":
            rec=df["Risk"].idxmin()

        elif risk=="Medium Risk":
            rec=(df["Profit Potential"]-df["Risk"]).idxmax()

        else:
            rec=df["Profit Potential"].idxmax()

        st.success(f"Recommended Stock Based on Risk: **{rec}**")

# =================================================
# TERMS PAGE
# =================================================

elif st.session_state.page == "terms":

    st.header("📚 Financial Terms")

    if st.button("⬅ Home"):
        st.session_state.page="home"

    for term,exp in financial_terms.items():

        with st.expander(term):
            st.write(exp)

# ------------------------------------------------
# Footer
# ------------------------------------------------

st.markdown("---")
st.write("⚠ Educational purpose only. Not financial advice.")