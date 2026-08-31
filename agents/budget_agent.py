def budget_agent(profile):
    income, expenses, debt, surplus = profile["income"], profile["expenses"], profile["debt"], profile["surplus"]
    findings = []
    if income == 0:
        findings.append({"severity":"warning","text":"Enter an income greater than zero for meaningful analysis."})
        return {"findings": findings}
    expense_ratio = expenses / income
    debt_ratio = debt / income
    if expense_ratio > 0.60:
        findings.append({"severity":"warning","text":f"Expenses are {expense_ratio*100:.1f}% of income; look for discretionary reductions."})
    else:
        findings.append({"severity":"good","text":f"Expenses are {expense_ratio*100:.1f}% of income."})
    if debt_ratio > 0.30:
        findings.append({"severity":"warning","text":f"Debt payments are {debt_ratio*100:.1f}% of income; avoid taking on unnecessary new debt."})
    else:
        findings.append({"severity":"good","text":f"Debt payments are {debt_ratio*100:.1f}% of income."})
    if surplus <= 0:
        findings.append({"severity":"warning","text":"There is no positive monthly surplus after expenses and debt."})
    else:
        findings.append({"severity":"good","text":f"Estimated monthly surplus is ₹{surplus:,.0f}."})
    return {"findings": findings}
