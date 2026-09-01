# Project Overview

**AI Financial Advisor Agent** is a multi-agent Streamlit dashboard for personal finance planning (educational, not regulated advice). A user enters income/expenses/savings/debt/goal data, and several rule-based "agents" analyze it:

- **profile_agent** — builds a structured profile + summary from the raw inputs
- **budget_agent** — flags budget warnings (overspending, high debt ratio, etc.)
- **goal_agent** — computes required monthly savings toward a goal and the gap vs. current surplus
- **investment_agent** — suggests investment categories based on risk preference
- **calculation_agent** — emergency fund target, debt-to-income ratio, EMI calculator
- **advisor_agent** — answers free-text questions using the other agents' outputs
- **coordinator** — synthesizes all agent outputs into one combined view

Data persists in a local SQLite db (`finance.db`) with a `users` table (auth) and `profiles` table (snapshot history per user).

## What's changed, in order

1. **Initial commit** — the core multi-agent Streamlit app.
2. **License/README/CI polish** — MIT license, badges, a CI check on `requirements.txt`.
3. **Admin/user roles** (`ff55c76`) — added SQLite-backed auth with two roles: `admin` can see every user's data via a read-only drill-in view; regular `user` only sees their own dashboard and gets a personal Advisor Agent tab.
4. **UI cleanup** (`3bc852b`) — hid the Goal Agent tab from a user's own dashboard (kept for admin's drill-in view).
5. **Password management** (`9dc95fe`) — the feature you just asked for:
   - **Change Password**: any logged-in user or admin gets a sidebar form to change their own password (must confirm current password first).
   - **Admin-assisted reset**: since there's no email service, admins can generate a one-time temporary password for any user from the admin dashboard and hand it off manually.
   - Login page now points forgetful users to "ask an admin to reset it."

## How it was verified

The app was run locally and the new `set_password` path was unit-tested directly against the real `finance.db` (old password rejected after reset, new one accepted), then the test account was cleaned up — the actual `admin` and `Novshita` accounts were untouched. The `.venv` has a stale shebang from before the project moved to OneDrive (`streamlit` binary points at a `Downloads` path that no longer exists); `python -m streamlit run app.py` works around it.

Both files are committed and pushed to `main` (`9dc95fe`).
