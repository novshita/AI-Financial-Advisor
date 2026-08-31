def monthly_goal_saving(target, months):
    return target / months if months else 0

def emi(principal, annual_rate, months):
    if months <= 0:
        return 0
    r = annual_rate / 12 / 100
    if r == 0:
        return principal / months
    return principal * r * (1+r)**months / ((1+r)**months - 1)

def financial_health_score(income, expenses, savings, debt):
    if income <= 0:
        return 0
    surplus = income - expenses - debt
    savings_rate = max(surplus/income, 0)
    debt_ratio = debt/income
    emergency_months = savings/max(expenses+debt, 1)
    score = 45
    score += min(savings_rate*100, 25)
    score += max(0, 20 - debt_ratio*50)
    score += min(emergency_months*3, 10)
    return int(max(0, min(100, round(score))))
