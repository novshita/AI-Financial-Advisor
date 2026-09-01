import secrets

import streamlit as st
import pandas as pd

from agents.profile_agent import profile_agent
from agents.budget_agent import budget_agent
from agents.goal_agent import goal_agent
from agents.investment_agent import investment_agent
from agents.calculation_agent import calculation_agent
from agents.advisor_agent import advisor_agent
from agents.coordinator import coordinator
from utils.calculations import financial_health_score, monthly_goal_saving, emi
from utils.db import (
    init_db,
    verify_user,
    create_user,
    username_exists,
    save_profile_snapshot,
    get_latest_profile,
    list_users_with_latest_snapshot,
    set_password,
)

st.set_page_config(page_title="AI Financial Advisor", page_icon="💰", layout="wide")
init_db()

if "user" not in st.session_state:
    st.session_state.user = None

RISK_OPTIONS = ["Conservative", "Moderate", "Aggressive"]


def render_login():
    st.title("💰 AI Financial Advisor")
    st.caption("Multi-agent personal finance planning dashboard")
    st.info("Educational project only: recommendations are general financial education, not guaranteed returns or regulated investment advice.")

    with st.form("login_form"):
        st.subheader("Log in")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log in")
        if submitted:
            user = verify_user(username, password)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with st.expander("Create account"):
        with st.form("signup_form"):
            new_username = st.text_input("Choose a username", key="signup_username")
            new_password = st.text_input("Choose a password", type="password", key="signup_password")
            signup_submitted = st.form_submit_button("Sign up")
            if signup_submitted:
                if not new_username or not new_password:
                    st.error("Username and password are required.")
                elif username_exists(new_username):
                    st.error("That username is already taken.")
                else:
                    create_user(new_username, new_password, "user")
                    st.success("Account created. You can log in now.")

    st.caption("Default admin login: **admin / admin123** (change after first login).")
    st.caption("Forgot your password? Ask an admin to reset it for you from the Admin dashboard.")


def render_change_password(user, key_prefix):
    with st.sidebar.expander("🔑 Change Password"):
        with st.form(f"change_password_form_{key_prefix}"):
            current_password = st.text_input("Current password", type="password", key=f"cur_pw_{key_prefix}")
            new_password = st.text_input("New password", type="password", key=f"new_pw_{key_prefix}")
            confirm_password = st.text_input("Confirm new password", type="password", key=f"confirm_pw_{key_prefix}")
            submitted = st.form_submit_button("Update password")
            if submitted:
                if not verify_user(user["username"], current_password):
                    st.error("Current password is incorrect.")
                elif not new_password:
                    st.error("New password cannot be empty.")
                elif new_password != confirm_password:
                    st.error("New password and confirmation do not match.")
                else:
                    set_password(user["id"], new_password)
                    st.success("Password updated.")


def render_dashboard(profile, budget, goal, investment, calc, *, editable, key_prefix, extra_tab_label=None):
    income, expenses, debt, savings = profile["income"], profile["expenses"], profile["debt"], profile["savings"]
    goal_name, goal_amount, goal_months, risk = profile["goal_name"], profile["goal_amount"], profile["goal_months"], profile["risk"]

    c1, c2, c3, c4 = st.columns(4)
    score = financial_health_score(income, expenses, savings, debt)
    c1.metric("Financial Health", f"{score}/100")
    c2.metric("Monthly Surplus", f"₹{max(income-expenses-debt,0):,.0f}")
    c3.metric("Savings Rate", f"{(max(income-expenses-debt,0)/income*100 if income else 0):.1f}%")
    c4.metric("Goal Saving Needed", f"₹{monthly_goal_saving(goal_amount, goal_months):,.0f}/mo")

    def render_overview():
        st.subheader("Financial Overview")
        st.dataframe(pd.DataFrame({
            "Metric": ["Monthly Income", "Monthly Expenses", "Monthly Debt", "Available Surplus", "Current Savings", "Goal"],
            "Value": [f"₹{income:,.0f}", f"₹{expenses:,.0f}", f"₹{debt:,.0f}", f"₹{max(income-expenses-debt,0):,.0f}", f"₹{savings:,.0f}", goal_name]
        }), width="stretch")
        st.progress(min(score/100, 1.0))
        st.write("**Profile:**", profile["summary"])

    def render_budget():
        st.subheader("Budget Analysis Agent")
        for item in budget["findings"]:
            st.write(("⚠️ " if item["severity"] == "warning" else "✅ ") + item["text"])
        st.bar_chart(pd.DataFrame({"Amount": [expenses, debt, max(income-expenses-debt, 0)]}, index=["Expenses", "Debt/EMI", "Surplus"]))

    def render_goal():
        st.subheader("Goal Planning Agent")
        st.write(f"**Goal:** {goal_name}")
        st.write(f"Target: **₹{goal_amount:,.0f}** in **{goal_months} months**")
        st.metric("Required monthly saving", f"₹{goal['required_monthly']:,.0f}")
        st.metric("Current estimated surplus", f"₹{goal['surplus']:,.0f}")
        if goal["gap"] > 0:
            st.warning(f"You have a monthly gap of ₹{goal['gap']:,.0f}. Consider extending the timeline, reducing expenses, or increasing income.")
        else:
            st.success("Your current surplus can cover the target under this simple no-return projection.")

    def render_investment():
        st.subheader("Investment Education Agent")
        st.write(f"Risk preference: **{risk}**")
        for item in investment:
            st.write(f"**{item['category']}** — {item['description']}")
        st.caption("Always verify current products, fees, taxes, suitability and regulations before investing.")

    def render_calculations():
        st.subheader("Financial Calculations")
        st.write(f"**Emergency-fund guideline:** ₹{calc['emergency_target']:,.0f} (3 months of core outgo estimate)")
        st.write(f"**Debt-to-income ratio:** {calc['debt_ratio']*100:.1f}%")
        st.write(f"**Goal monthly saving:** ₹{calc['goal_monthly']:,.0f}")
        st.divider()
        st.markdown("### EMI Calculator")
        if editable:
            loan = st.number_input("Loan principal (₹)", 0.0, 5000000.0, 500000.0, 10000.0, key=f"loan_{key_prefix}")
            rate = st.number_input("Annual interest rate (%)", 0.0, 50.0, 10.0, 0.5, key=f"rate_{key_prefix}")
            months = st.number_input("Loan tenure (months)", 1, 360, 60, 1, key=f"months_{key_prefix}")
            st.metric("Estimated EMI", f"₹{emi(loan, rate, months):,.0f}")
        else:
            st.caption("The EMI calculator is available on each user's own dashboard.")

    def render_coordinator():
        st.subheader("Multi-Agent Coordinator")
        st.markdown(coordinator(profile, budget, goal, investment, calc))

    tab_defs = [("📊 Overview", render_overview), ("💸 Budget Agent", render_budget)]
    if not editable:
        # Goal Agent stays available to admin's read-only drill-in view, but is
        # hidden from a user's own dashboard.
        tab_defs.append(("🎯 Goal Agent", render_goal))
    tab_defs += [
        ("📈 Investment Agent", render_investment),
        ("🧮 Calculations", render_calculations),
        ("🤖 AI Coordinator", render_coordinator),
    ]

    labels = [label for label, _ in tab_defs] + ([extra_tab_label] if extra_tab_label else [])
    tabs = st.tabs(labels)
    for tab, (_, render_fn) in zip(tabs, tab_defs):
        with tab:
            render_fn()

    return tabs[len(tab_defs)] if extra_tab_label else None


def render_advisor_tab(tab, user, profile, budget, goal, investment, calc):
    with tab:
        st.subheader("🧑‍💼 Advisor Agent")
        st.caption("Ask a question about your finances. This agent reasons over your profile, budget, goal, investment and calculation agents' outputs to answer.")

        history_key = f"advisor_history_{user['id']}"
        if history_key not in st.session_state:
            st.session_state[history_key] = []

        with st.form(f"advisor_form_{user['id']}"):
            question = st.text_input("Your question", placeholder="e.g. How can I save more money?")
            asked = st.form_submit_button("Ask")

        if asked and question.strip():
            answer = advisor_agent(question, profile, budget, goal, investment, calc)
            st.session_state[history_key].append((question, answer))

        for q, a in reversed(st.session_state[history_key]):
            st.markdown(f"**You:** {q}")
            st.markdown(f"**Advisor:** {a}")
            st.divider()


def render_user_view(user):
    st.sidebar.write(f"👤 Logged in as **{user['username']}** ({user['role']})")
    render_change_password(user, key_prefix="user")
    if st.sidebar.button("Log out", key="logout_user"):
        st.session_state.user = None
        st.rerun()

    st.title("💰 AI Financial Advisor")
    st.caption("Multi-agent personal finance planning dashboard")
    st.info("Educational project only: recommendations are general financial education, not guaranteed returns or regulated investment advice.")

    latest = get_latest_profile(user["id"])
    defaults = latest or {
        "income": 50000.0, "expenses": 30000.0, "savings": 100000.0, "debt": 5000.0,
        "goal_name": "Emergency Fund", "goal_amount": 150000.0, "goal_months": 12, "risk": "Conservative",
    }

    with st.sidebar.form("profile_form"):
        st.header("👤 Financial Profile")
        income = st.number_input("Monthly income (₹)", min_value=0.0, value=float(defaults["income"]), step=1000.0)
        expenses = st.number_input("Monthly expenses (₹)", min_value=0.0, value=float(defaults["expenses"]), step=1000.0)
        savings = st.number_input("Current savings (₹)", min_value=0.0, value=float(defaults["savings"]), step=5000.0)
        debt = st.number_input("Monthly EMI/debt payment (₹)", min_value=0.0, value=float(defaults["debt"]), step=500.0)
        goal_name = st.text_input("Financial goal", defaults["goal_name"])
        goal_amount = st.number_input("Goal amount (₹)", min_value=0.0, value=float(defaults["goal_amount"]), step=5000.0)
        goal_months = st.number_input("Goal timeline (months)", min_value=1, value=int(defaults["goal_months"]), step=1)
        risk_index = RISK_OPTIONS.index(defaults["risk"]) if defaults["risk"] in RISK_OPTIONS else 0
        risk = st.selectbox("Risk preference", RISK_OPTIONS, index=risk_index)
        submitted = st.form_submit_button("🚀 Analyze My Finances", width="stretch")

    session_key = f"profile_{user['id']}"
    if submitted:
        profile = profile_agent(income, expenses, savings, debt, goal_name, goal_amount, goal_months, risk)
        save_profile_snapshot(user["id"], profile)
        st.session_state[session_key] = profile
    elif session_key not in st.session_state and latest:
        st.session_state[session_key] = profile_agent(
            latest["income"], latest["expenses"], latest["savings"], latest["debt"],
            latest["goal_name"], latest["goal_amount"], latest["goal_months"], latest["risk"],
        )

    profile = st.session_state.get(session_key)
    if profile is None:
        st.write("Fill in your financial profile in the sidebar and click **Analyze My Finances** to get started.")
        return

    budget = budget_agent(profile)
    goal = goal_agent(profile)
    investment = investment_agent(profile)
    calc = calculation_agent(profile)

    advisor_tab = render_dashboard(
        profile, budget, goal, investment, calc,
        editable=True, key_prefix="self", extra_tab_label="🧑‍💼 Advisor Agent",
    )
    render_advisor_tab(advisor_tab, user, profile, budget, goal, investment, calc)


def render_admin_view(user):
    st.sidebar.write(f"👤 Logged in as **{user['username']}** ({user['role']})")
    render_change_password(user, key_prefix="admin")
    if st.sidebar.button("Log out", key="logout_admin"):
        st.session_state.user = None
        st.rerun()

    st.title("💰 AI Financial Advisor — Admin")
    st.caption("Multi-agent personal finance planning dashboard")

    users = list_users_with_latest_snapshot()
    table_rows = []
    for u in users:
        surplus = health = None
        if u["income"] is not None:
            surplus = max(u["income"] - (u["expenses"] or 0) - (u["debt"] or 0), 0)
            health = financial_health_score(u["income"], u["expenses"] or 0, u["savings"] or 0, u["debt"] or 0)
        table_rows.append({
            "Username": u["username"],
            "Role": u["role"],
            "Joined": u["created_at"][:10],
            "Monthly Income": f"₹{u['income']:,.0f}" if u["income"] is not None else "—",
            "Monthly Surplus": f"₹{surplus:,.0f}" if surplus is not None else "—",
            "Financial Health": f"{health}/100" if health is not None else "—",
            "Last Updated": u["snapshot_at"][:10] if u["snapshot_at"] else "—",
        })

    st.subheader("All users")
    st.dataframe(pd.DataFrame(table_rows), width="stretch")

    non_admins = [u for u in users if u["role"] == "user"]
    if not non_admins:
        st.info("No regular users have signed up yet.")
        return

    st.subheader("View a user's dashboard")
    selected_username = st.selectbox("Select user", [u["username"] for u in non_admins])
    selected = next(u for u in non_admins if u["username"] == selected_username)

    with st.expander(f"🔑 Reset password for {selected_username}"):
        st.caption("Generates a new temporary password. Share it with the user securely; they should change it after logging in.")
        if st.button("Generate temporary password", key=f"reset_pw_{selected['id']}"):
            temp_password = secrets.token_urlsafe(6)
            set_password(selected["id"], temp_password)
            st.success(f"New temporary password for **{selected_username}**: `{temp_password}`")

    if selected["income"] is None:
        st.info(f"{selected_username} hasn't submitted any financial data yet.")
        return

    profile = profile_agent(
        selected["income"], selected["expenses"], selected["savings"], selected["debt"],
        selected["goal_name"], selected["goal_amount"], selected["goal_months"], selected["risk"],
    )
    budget = budget_agent(profile)
    goal = goal_agent(profile)
    investment = investment_agent(profile)
    calc = calculation_agent(profile)

    render_dashboard(
        profile, budget, goal, investment, calc,
        editable=False, key_prefix=f"user_{selected['id']}",
    )


current_user = st.session_state.user
if current_user is None:
    render_login()
elif current_user["role"] == "admin":
    render_admin_view(current_user)
else:
    render_user_view(current_user)
