import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import json, os

from agents.profile_agent import profile_agent
from agents.budget_agent import budget_agent
from agents.goal_agent import goal_agent
from agents.investment_agent import investment_agent
from agents.calculation_agent import calculation_agent
from agents.coordinator import coordinator
from utils.calculations import financial_health_score, monthly_goal_saving, emi

st.set_page_config(page_title="AI Financial Advisor", page_icon="💰", layout="wide")

st.title("💰 AI Financial Advisor")
st.caption("Multi-agent personal finance planning dashboard")

with st.sidebar:
    st.header("👤 Financial Profile")
    income = st.number_input("Monthly income (₹)", min_value=0.0, value=50000.0, step=1000.0)
    expenses = st.number_input("Monthly expenses (₹)", min_value=0.0, value=30000.0, step=1000.0)
    savings = st.number_input("Current savings (₹)", min_value=0.0, value=100000.0, step=5000.0)
    debt = st.number_input("Monthly EMI/debt payment (₹)", min_value=0.0, value=5000.0, step=500.0)
    goal_name = st.text_input("Financial goal", "Emergency Fund")
    goal_amount = st.number_input("Goal amount (₹)", min_value=0.0, value=150000.0, step=5000.0)
    goal_months = st.number_input("Goal timeline (months)", min_value=1, value=12, step=1)
    risk = st.selectbox("Risk preference", ["Conservative", "Moderate", "Aggressive"])
    analyze = st.button("🚀 Analyze My Finances", use_container_width=True)

st.info("Educational project only: recommendations are general financial education, not guaranteed returns or regulated investment advice.")

profile = profile_agent(income, expenses, savings, debt, goal_name, goal_amount, goal_months, risk)
budget = budget_agent(profile)
goal = goal_agent(profile)
investment = investment_agent(profile)
calc = calculation_agent(profile)

c1, c2, c3, c4 = st.columns(4)
score = financial_health_score(income, expenses, savings, debt)
c1.metric("Financial Health", f"{score}/100")
c2.metric("Monthly Surplus", f"₹{max(income-expenses-debt,0):,.0f}")
c3.metric("Savings Rate", f"{(max(income-expenses-debt,0)/income*100 if income else 0):.1f}%")
c4.metric("Goal Saving Needed", f"₹{monthly_goal_saving(goal_amount, goal_months):,.0f}/mo")

tabs = st.tabs(["📊 Overview", "💸 Budget Agent", "🎯 Goal Agent", "📈 Investment Agent", "🧮 Calculations", "🤖 AI Coordinator"])

with tabs[0]:
    st.subheader("Financial Overview")
    st.dataframe(pd.DataFrame({
        "Metric": ["Monthly Income","Monthly Expenses","Monthly Debt","Available Surplus","Current Savings","Goal"],
        "Value": [f"₹{income:,.0f}",f"₹{expenses:,.0f}",f"₹{debt:,.0f}",f"₹{max(income-expenses-debt,0):,.0f}",f"₹{savings:,.0f}",goal_name]
    }), use_container_width=True)
    st.progress(min(score/100,1.0))
    st.write("**Profile:**", profile["summary"])

with tabs[1]:
    st.subheader("Budget Analysis Agent")
    for item in budget["findings"]:
        st.write(("⚠️ " if item["severity"]=="warning" else "✅ ") + item["text"])
    st.bar_chart(pd.DataFrame({"Amount":[expenses, debt, max(income-expenses-debt,0)]}, index=["Expenses","Debt/EMI","Surplus"]))

with tabs[2]:
    st.subheader("Goal Planning Agent")
    st.write(f"**Goal:** {goal_name}")
    st.write(f"Target: **₹{goal_amount:,.0f}** in **{goal_months} months**")
    st.metric("Required monthly saving", f"₹{goal['required_monthly']:,.0f}")
    st.metric("Current estimated surplus", f"₹{goal['surplus']:,.0f}")
    if goal["gap"] > 0:
        st.warning(f"You have a monthly gap of ₹{goal['gap']:,.0f}. Consider extending the timeline, reducing expenses, or increasing income.")
    else:
        st.success("Your current surplus can cover the target under this simple no-return projection.")

with tabs[3]:
    st.subheader("Investment Education Agent")
    st.write(f"Risk preference: **{risk}**")
    for item in investment:
        st.write(f"**{item['category']}** — {item['description']}")
    st.caption("Always verify current products, fees, taxes, suitability and regulations before investing.")

with tabs[4]:
    st.subheader("Financial Calculations")
    st.write(f"**Emergency-fund guideline:** ₹{calc['emergency_target']:,.0f} (3 months of core outgo estimate)")
    st.write(f"**Debt-to-income ratio:** {calc['debt_ratio']*100:.1f}%")
    st.write(f"**Goal monthly saving:** ₹{calc['goal_monthly']:,.0f}")
    st.divider()
    st.markdown("### EMI Calculator")
    loan = st.number_input("Loan principal (₹)", 0.0, 5000000.0, 500000.0, 10000.0, key="loan")
    rate = st.number_input("Annual interest rate (%)", 0.0, 50.0, 10.0, 0.5, key="rate")
    months = st.number_input("Loan tenure (months)", 1, 360, 60, 1, key="months")
    st.metric("Estimated EMI", f"₹{emi(loan, rate, months):,.0f}")

with tabs[5]:
    st.subheader("Multi-Agent Coordinator")
    if analyze:
        result = coordinator(profile, budget, goal, investment, calc)
        st.success("Analysis completed by the agent workflow.")
        st.markdown(result)
    else:
        st.write("Click **Analyze My Finances** in the sidebar to run the coordinator.")

st.divider()
st.caption("AI Financial Advisor • BCA AI & Data Analytics Project")
