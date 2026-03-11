def analyze_financial_profile(income, expenses, savings, risk_tolerance, investment_goal, horizon):
    """
    Analyze user's financial condition
    """

    # Calculate disposable income
    disposable_income = income - expenses

    # Recommended investment amount (30% rule)
    recommended_investment = disposable_income * 0.30

    # Financial health score
    savings_ratio = savings / income if income > 0 else 0
    financial_health_score = min(100, savings_ratio * 100)

    # Investor classification
    if risk_tolerance == "low":
        investor_type = "Conservative"

    elif risk_tolerance == "medium":
        investor_type = "Moderate"

    else:
        investor_type = "Aggressive"

    # Investment horizon classification
    if horizon < 3:
        horizon_type = "Short Term"

    elif horizon < 7:
        horizon_type = "Medium Term"

    else:
        horizon_type = "Long Term"

    return {
        "Disposable Income": disposable_income,
        "Recommended Investment": recommended_investment,
        "Financial Health Score": financial_health_score,
        "Investor Type": investor_type,
        "Investment Horizon": horizon_type,
        "Goal": investment_goal
    }