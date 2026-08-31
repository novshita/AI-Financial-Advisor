def calculation_agent(profile):
    income, expenses, debt = profile["income"], profile["expenses"], profile["debt"]
    from utils.calculations import monthly_goal_saving
    return {
        "emergency_target": max((expenses + debt) * 3, 0),
        "debt_ratio": debt / income if income else 0,
        "goal_monthly": monthly_goal_saving(profile["goal_amount"], profile["goal_months"])
    }
