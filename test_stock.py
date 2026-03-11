from modules.stock_data import get_stock_data
import matplotlib.pyplot as plt

data = get_stock_data("AAPL")

plt.figure(figsize=(10,5))

plt.plot(data["Close"])

plt.title("Apple Stock Price")

plt.xlabel("Date")

plt.ylabel("Price")

plt.show()