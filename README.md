# AI Study Assistant

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-web%20framework-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-Responses%20API-412991?logo=openai&logoColor=white)](https://platform.openai.com/docs/api-reference/responses)

This is a Flask app that creates quiz questions, concise summaries, and study plans with OpenAI.

**Tech stack:** Python, Flask, OpenAI Responses API (`gpt-4o-mini`), HTML, CSS.

## Preview

Animated preview using Model Context Protocol (MCP) as the topic, cycling through quiz, summary, and study-plan outputs:

![AI Study Assistant showing quiz, summary, and study plan examples for Model Context Protocol](screenshots/mcp-study-modes-demo.gif)

## Setup

```powershell
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your OpenAI API key to `.env`:

```text
OPENAI_API_KEY=your_api_key_here
```

Run the app:

```powershell
python app.py
```

Open http://localhost:5000. Keep `.env` private; it is excluded from Git.
