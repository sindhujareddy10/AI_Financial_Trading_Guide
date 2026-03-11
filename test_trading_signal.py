from modules.stock_data import get_stock_data
from modules.trading_signals import generate_trading_signal


data = get_stock_data("AAPL")

signal = generate_trading_signal(data)

print("Trading Signal:", signal)