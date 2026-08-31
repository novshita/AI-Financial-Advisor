# AI Financial Advisor — Multi-Agent Project

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-app-ff4b4b.svg)](https://streamlit.io/)
[![Last Commit](https://img.shields.io/github/last-commit/novshita/AI-Financial-Advisor.svg)](https://github.com/novshita/AI-Financial-Advisor/commits/main)

A ready-to-run BCA AI & Data Analytics project built with Python and Streamlit.

## Features
- Financial profile agent
- Budget analysis agent
- Goal planning agent
- Investment education agent
- Financial calculation agent
- Multi-agent coordinator
- Financial health score
- EMI calculator
- Goal-based monthly saving calculator
- Interactive Streamlit dashboard
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
│   └── coordinator.py
└── utils/
    ├── __init__.py
    └── calculations.py
```

## How it is agentic

The coordinator passes the user's financial profile through multiple specialized agents. Each agent performs a distinct task, and the coordinator combines their outputs into a final planning report.

## Future upgrades
- Add an LLM API for natural-language conversations.
- Add CSV expense upload and automatic categorization.
- Add SQLite user profiles and history.
- Add charts for spending trends.
- Add current market/news data only from trusted sources.
- Add authentication.
- Add PDF report generation.

## Disclaimer
This application is for education and demonstration. It does not guarantee returns and should not be treated as regulated financial advice.
