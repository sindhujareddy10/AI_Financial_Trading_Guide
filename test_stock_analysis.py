from modules.stock_data import get_stock_data
from modules.stock_analysis import calculate_returns, moving_average, trend_analysis
import matplotlib.pyplot as plt


# Get stock data
data = get_stock_data("AAPL")

# Calculate returns
avg_return, volatility = calculate_returns(data)

# Calculate moving averages
data = moving_average(data)

# Detect trend
trend = trend_analysis(data)

print("Average Return:", avg_return)
print("Volatility:", volatility)
print("Market Trend:", trend)


# Plot chart
plt.figure(figsize=(10,5))

plt.plot(data["Close"], label="Price")
plt.plot(data["MA50"], label="MA50")
plt.plot(data["MA200"], label="MA200")

plt.title("Stock Trend Analysis")
plt.xlabel("Date")
plt.ylabel("Price")

plt.legend()

plt.show()