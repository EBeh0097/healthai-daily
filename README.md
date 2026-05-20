# HealthAI Daily — Phase 1 MVP

This MVP creates a source-grounded healthcare AI news dashboard.

## What it does

- Searches healthcare AI news using SerpAPI
- Collects source URLs, dates, snippets, and titles
- Ranks stories by relevance and credibility
- Generates fact-check notes
- Creates YouTube Shorts scripts with citations
- Displays everything in Streamlit

## Required secrets

Store these in Google Secret Manager or Streamlit Secrets:

- OPENAI_API_KEY
- SERPAPI_API_KEY
- GOOGLE_CLOUD_PROJECT_ID

## Local run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Safety rule

No source URL = no script.
Every report must include citations.
