# modules/alerts.py
def generate_alert(stock, ma50, ma200):
    if ma50 > ma200:
        return f"{stock}: Bullish Signal – Consider BUY"
    else:
        return f"{stock}: Bearish Signal – Consider SELL"