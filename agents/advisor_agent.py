KEYWORD_GROUPS = [
    ("debt", ["debt", "loan", "emi"]),
    ("invest", ["invest", "investment", "risk"]),
    ("emergency", ["emergency"]),
    ("save", ["save", "saving", "savings"]),
]


def _debt_advice(profile, budget, calc):
    lines = [f"Your debt payments are about **{calc['debt_ratio']*100:.1f}%** of income."]
    for item in budget["findings"]:
        if "debt" in item["text"].lower():
            lines.append(item["text"])
    return " ".join(lines)


def _invest_advice(profile, investment):
    lines = [f"Based on your **{profile['risk']}** risk preference:"]
    for item in investment:
        lines.append(f"- **{item['category']}**: {item['description']}")
    return "\n".join(lines)


def _emergency_advice(profile, calc):
    gap = max(calc["emergency_target"] - profile["savings"], 0)
    if gap > 0:
        return (
            f"A 3-month emergency fund target is about ₹{calc['emergency_target']:,.0f}. "
            f"You currently have ₹{profile['savings']:,.0f} saved, so you're about "
            f"₹{gap:,.0f} short of that cushion."
        )
    return (
        f"A 3-month emergency fund target is about ₹{calc['emergency_target']:,.0f}, "
        f"and your current savings of ₹{profile['savings']:,.0f} already cover it."
    )


def _save_advice(profile, budget, goal):
    lines = [
        f"To reach **{profile['goal_name']}** in {profile['goal_months']} months, "
        f"aim to save about ₹{goal['required_monthly']:,.0f}/month."
    ]
    if goal["gap"] > 0:
        lines.append(
            f"Your current surplus falls short by ₹{goal['gap']:,.0f}/month — "
            "consider trimming discretionary expenses or extending the timeline."
        )
    for item in budget["findings"]:
        if item["severity"] == "warning":
            lines.append(item["text"])
    return " ".join(lines)


def _fallback_advice(budget):
    lines = ["Here's a general read on your finances:"]
    for item in budget["findings"]:
        lines.append(("⚠️ " if item["severity"] == "warning" else "✅ ") + item["text"])
    lines.append("Ask about **saving**, **debt**, **investing**, or your **emergency fund** for more specific advice.")
    return "\n".join(lines)


def advisor_agent(question, profile, budget, goal, investment, calc):
    q = question.lower()
    handlers = {
        "debt": lambda: _debt_advice(profile, budget, calc),
        "invest": lambda: _invest_advice(profile, investment),
        "emergency": lambda: _emergency_advice(profile, calc),
        "save": lambda: _save_advice(profile, budget, goal),
    }
    for key, keywords in KEYWORD_GROUPS:
        if any(kw in q for kw in keywords):
            return handlers[key]()
    return _fallback_advice(budget)
