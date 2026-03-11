from modules.stock_data import get_stock_data
from modules.stock_analysis import calculate_returns


def recommend_stocks(risk_level):

    # Beginner-friendly stocks
    stocks = [
        "AAPL",
        "MSFT",
        "GOOGL",
        "AMZN",
        "NVDA"
    ]

    recommendations = []

    for stock in stocks:

        try:
            data = get_stock_data(stock)

            avg_return, volatility = calculate_returns(data)

            score = avg_return - volatility

            recommendations.append({
                "stock": stock,
                "return": avg_return,
                "risk": volatility,
                "score": score
            })

        except:
            continue

    # Sort by best score
    recommendations = sorted(
        recommendations,
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations[:3]