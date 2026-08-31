def coordinator(profile, budget, goal, investment, calc):
    lines = [
        "### 🧠 Coordinator Report",
        f"**1. Financial snapshot:** {profile['summary']}",
        f"**2. Budget:** Your estimated monthly surplus is **₹{profile['surplus']:,.0f}**.",
        f"**3. Goal:** Save about **₹{goal['required_monthly']:,.0f}/month** to reach **₹{profile['goal_name']}** in {profile['goal_months']} months under a simple no-return calculation.",
        f"**4. Emergency fund:** A basic 3-month target from current expenses + debt is about **₹{calc['emergency_target']:,.0f}**.",
        f"**5. Risk profile:** {profile['risk']}. Investment information should be matched to time horizon and ability to tolerate losses.",
        "**6. Next actions:** Build/maintain emergency savings, track discretionary spending, automate goal savings, and review debt costs.",
        "",
        "> This is a student-project financial planning tool and not personalized regulated investment advice."
    ]
    return "\n\n".join(lines)
