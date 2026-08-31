from utils.calculations import monthly_goal_saving

def goal_agent(profile):
    required = monthly_goal_saving(profile["goal_amount"], profile["goal_months"])
    surplus = profile["surplus"]
    return {"required_monthly": required, "surplus": surplus, "gap": max(required-surplus,0)}
