# modules/stock_analysis.py
import pandas as pd
import numpy as np

def moving_averages(data):
    data["MA50"] = data["Close"].rolling(50).mean()
    data["MA200"] = data["Close"].rolling(200).mean()
    return data

def calculate_returns(data):
    data["returns"] = data["Close"].pct_change()
    avg_return = data["returns"].mean() * 252  # annualized
    volatility = data["returns"].std() * np.sqrt(252)
    return avg_return, volatility

def calculate_rsi(data, window=14):
    delta = data["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    data["RSI"] = rsi
    return data

def market_trend(data):
    ma50 = data["MA50"].iloc[-1]
    ma200 = data["MA200"].iloc[-1]
    if ma50 > ma200:
        return "Bullish 📈"
    elif ma50 < ma200:
        return "Bearish 📉"
    else:
        return "Sideways"