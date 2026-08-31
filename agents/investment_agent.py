def investment_agent(profile):
    risk = profile["risk"]
    if risk == "Conservative":
        return [
            {"category":"Emergency savings","description":"Prioritize a liquid emergency reserve before taking meaningful market risk."},
            {"category":"Lower-volatility options","description":"Learn about deposits and high-quality fixed-income instruments; compare liquidity, tax and issuer risk."},
            {"category":"Diversified investing","description":"If appropriate, consider diversified products after understanding risk and costs."},
        ]
    if risk == "Aggressive":
        return [
            {"category":"Diversification","description":"Learn how diversified equity-oriented investments can provide long-term growth with higher volatility."},
            {"category":"Risk control","description":"Keep an emergency reserve and avoid concentrating the portfolio in one asset or company."},
            {"category":"Long-term focus","description":"Use a long horizon and understand drawdowns before accepting higher risk."},
        ]
    return [
        {"category":"Balanced diversification","description":"Consider learning about a mix of growth-oriented and lower-volatility assets based on time horizon."},
        {"category":"Emergency reserve","description":"Build liquid savings before allocating money needed in the near term to volatile assets."},
        {"category":"Periodic review","description":"Review allocation, fees, taxes and goals periodically rather than reacting to short-term market moves."},
    ]
