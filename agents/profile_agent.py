def profile_agent(income, expenses, savings, debt, goal_name, goal_amount, goal_months, risk):
    surplus = max(income - expenses - debt, 0)
    return {
        "income": income, "expenses": expenses, "savings": savings, "debt": debt,
        "goal_name": goal_name, "goal_amount": goal_amount, "goal_months": goal_months,
        "risk": risk, "surplus": surplus,
        "summary": f"Income ₹{income:,.0f}, expenses ₹{expenses:,.0f}, debt ₹{debt:,.0f}, savings ₹{savings:,.0f}, risk profile {risk}."
    }
