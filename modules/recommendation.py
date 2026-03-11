# modules/recommendation.py
def recommend_stocks(risk_level):
    if risk_level == "Low":
        return ["JNJ", "PG", "KO", "PEP"]
    elif risk_level == "Medium":
        return ["AAPL", "MSFT", "GOOGL", "NVDA"]
    else:
        return ["TSLA", "AMD", "NVDA", "META"]