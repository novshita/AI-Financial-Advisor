# AI Financial Advisor — Multi-Agent Project

[![CI](https://github.com/novshita/AI-Financial-Advisor/actions/workflows/ci.yml/badge.svg)](https://github.com/novshita/AI-Financial-Advisor/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-app-ff4b4b.svg)](https://streamlit.io/)
[![Last Commit](https://img.shields.io/github/last-commit/novshita/AI-Financial-Advisor.svg)](https://github.com/novshita/AI-Financial-Advisor/commits/main)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A ready-to-run BCA AI & Data Analytics project built with Python and Streamlit.

## Features
- Financial profile agent
- Budget analysis agent
- Goal planning agent
- Investment education agent
- Financial calculation agent
- Advisor agent — answers free-text questions using the other agents' outputs
- Multi-agent coordinator
- Financial health score
- EMI calculator
- Goal-based monthly saving calculator
- Interactive Streamlit dashboard
- Admin and user accounts backed by SQLite, with role-based access
- Change password (self-service) and admin-assisted password reset
- No API key required for the included rule-based demo

## Run locally

### Windows
1. Install Python 3.10+.
2. Open this project folder in VS Code.
3. Open Terminal.
4. Run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

5. Open the local URL shown by Streamlit, normally:
`http://localhost:8501`

A local `finance.db` SQLite file is created automatically on first run (git-ignored).

## Accounts & roles

- **Admin**: a default admin account is seeded on first run — `admin` / `admin123`. Change this password after first login if you deploy this anywhere shared. Admins see every user's data: a table of all users with their latest financial snapshot, and can drill into any individual user's dashboard read-only. Admins do not have their own financial profile or access to the Advisor Agent tab.
- **User**: sign up via "Create account" on the login screen. A user only sees their own financial profile and history, and gets an "🧑‍💼 Advisor Agent" tab that admins do not have.

Passwords are stored as PBKDF2-HMAC-SHA256 hashes with a per-user salt (stdlib `hashlib`/`secrets` — no extra dependency).

## Password management

- **Change password**: any logged-in user or admin can open "🔑 Change Password" in the sidebar, confirm their current password, and set a new one.
- **Forgot password**: there's no email service in this app, so self-service reset isn't available. Instead, an admin can open "🔑 Reset password for `<user>`" on the Admin dashboard to generate a one-time temporary password and hand it to the user, who should change it after logging in.

## Project structure

```text
AI_Financial_Advisor_Agent/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── agents/
│   ├── __init__.py
│   ├── profile_agent.py
│   ├── budget_agent.py
│   ├── goal_agent.py
│   ├── investment_agent.py
│   ├── calculation_agent.py
│   ├── advisor_agent.py
│   └── coordinator.py
└── utils/
    ├── __init__.py
    ├── calculations.py
    └── db.py
```

## How it is agentic

The coordinator passes the user's financial profile through multiple specialized agents. Each agent performs a distinct task, and the coordinator combines their outputs into a final planning report. The Advisor Agent adds a question-driven layer on top: it parses a user's free-text question for intent (saving, debt, investing, or emergency fund) and composes an answer from whichever of the other agents' outputs is most relevant — no LLM or API key involved.

## Future upgrades
- Add an LLM API for natural-language conversations.
- Add CSV expense upload and automatic categorization.
- Add charts for spending trends.
- Add current market/news data only from trusted sources.
- Add PDF report generation.

## Disclaimer
This application is for education and demonstration. It does not guarantee returns and should not be treated as regulated financial advice.
