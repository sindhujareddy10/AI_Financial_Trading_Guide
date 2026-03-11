import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Trading Simulator", layout="wide")

st.title("🎮 Beginner Trading Simulator")

st.write("Practice trading with virtual money using real-time stock data.")

# -------------------------
# Session variables
# -------------------------

if "balance" not in st.session_state:
    st.session_state.balance = 10000

if "portfolio" not in st.session_state:
    st.session_state.portfolio = {}

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "level" not in st.session_state:
    st.session_state.level = 1


# -------------------------
# XP System
# -------------------------

def add_xp(points):
    st.session_state.xp += points
    
    if st.session_state.xp > 100:
        st.session_state.level += 1
        st.session_state.xp = 0
        st.success("🎉 Level Up! You are now Level " + str(st.session_state.level))


# -------------------------
# Sidebar Stats
# -------------------------

st.sidebar.header("🏆 Player Stats")

st.sidebar.write("💰 Balance:", round(st.session_state.balance,2))
st.sidebar.write("⭐ XP:", st.session_state.xp)
st.sidebar.write("🏅 Level:", st.session_state.level)


# -------------------------
# Stock Selection
# -------------------------

st.header("📈 Choose a Stock")

symbol = st.text_input("Enter Stock Symbol (Example: AAPL, TSLA, MSFT)", "AAPL")

stock = yf.Ticker(symbol)
data = stock.history(period="6mo")

if data.empty:
    st.error("Stock not found")
    st.stop()

price = data["Close"].iloc[-1]

st.metric("Current Price", "$"+str(round(price,2)))

# -------------------------
# Chart
# -------------------------

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=data.index,
    y=data["Close"],
    mode="lines",
    name="Stock Price"
))

fig.update_layout(title="Stock Price Trend")

st.plotly_chart(fig,use_container_width=True)

# -------------------------
# Trading
# -------------------------

st.header("💸 Trade Stock")

quantity = st.number_input("How many shares do you want?",1)

cost = quantity * price

col1,col2 = st.columns(2)

# BUY

if col1.button("BUY"):
    
    if st.session_state.balance >= cost:
        
        st.session_state.balance -= cost
        
        if symbol in st.session_state.portfolio:
            st.session_state.portfolio[symbol] += quantity
        else:
            st.session_state.portfolio[symbol] = quantity
            
        add_xp(20)
        
        st.success("Stock purchased!")
        
    else:
        st.error("Not enough balance")

# SELL

if col2.button("SELL"):
    
    if symbol in st.session_state.portfolio:
        
        owned = st.session_state.portfolio[symbol]
        
        if owned >= quantity:
            
            st.session_state.balance += cost
            st.session_state.portfolio[symbol] -= quantity
            
            add_xp(15)
            
            st.success("Stock sold!")
            
        else:
            st.error("You don't own enough shares")
    else:
        st.error("You don't own this stock")

# -------------------------
# Portfolio
# -------------------------

st.header("📊 Your Portfolio")

portfolio_data = []

for stock_symbol,qty in st.session_state.portfolio.items():
    
    stock_price = yf.Ticker(stock_symbol).history(period="1d")["Close"].iloc[-1]
    
    value = stock_price * qty
    
    portfolio_data.append({
        "Stock":stock_symbol,
        "Shares":qty,
        "Price":round(stock_price,2),
        "Value":round(value,2)
    })

if portfolio_data:
    df = pd.DataFrame(portfolio_data)
    st.dataframe(df)
else:
    st.write("No investments yet")

# -------------------------
# Beginner Learning Section
# -------------------------

st.header("📚 Beginner Trading Tips")

tips = [
"📌 Buy stocks when prices are lower than recent averages.",
"📌 Diversify investments across multiple companies.",
"📌 Avoid investing all money in one stock.",
"📌 Long term investing is safer than frequent trading."
]

for t in tips:
    st.info(t)

# -------------------------
# Daily Challenge
# -------------------------

st.header("🎯 Daily Challenge")

st.write("Make a profit of **$200** using virtual trading!")

if st.session_state.balance > 10200:
    st.success("🏆 Challenge Completed!")