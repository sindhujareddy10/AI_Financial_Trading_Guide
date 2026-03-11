import pandas as pd

def simulate_portfolio_growth(investment, years, expected_return=0.12):

    values = []

    for year in range(1, years + 1):

        future_value = investment * ((1 + expected_return) ** year)

        values.append({
            "Year": year,
            "Portfolio Value": future_value
        })

    df = pd.DataFrame(values)

    return df