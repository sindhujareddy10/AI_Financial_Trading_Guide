from modules.financial_profile import analyze_financial_profile

profile = analyze_financial_profile(
    income=50000,
    expenses=30000,
    savings=200000,
    risk_tolerance="medium",
    investment_goal="Wealth Growth",
    horizon=5
)

print(profile)