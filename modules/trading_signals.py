import pandas as pd


def generate_trading_signal(data):

    # Moving averages
    data["MA50"] = data["Close"].rolling(window=50).mean()
    data["MA200"] = data["Close"].rolling(window=200).mean()

    latest_ma50 = data["MA50"].iloc[-1]
    latest_ma200 = data["MA200"].iloc[-1]

    # Generate signal
    if latest_ma50 > latest_ma200:
        signal = "BUY"

    elif latest_ma50 < latest_ma200:
        signal = "SELL"

    else:
        signal = "HOLD"

    return signal