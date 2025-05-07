import requests
import os
import re
import json
from dotenv import load_dotenv

load_dotenv()

def clean_json_response(raw_text):
    match = re.search(r'\[.*\]', raw_text, re.DOTALL)
    return match.group(0) if match else "[]"

def query_groq(text):
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }

    prompt = f"""Given this content:

{text}

Return up to 5 charts as a raw JSON array.
Each chart should follow this format:
{{
  "type": "bar" | "line" | "pie",
  "title": "...",
  "x": [...],
  "y": [...]
}}

Guidelines:
- Use "bar" or "line" for time-series data like Revenue, ARPU, Subscribers, Churn.
- Use "pie" only when representing parts of a whole (e.g. Revenue Breakdown, Expense Distribution).
- Titles must clearly describe the chart content.
- Only include well-structured charts (x and y must be arrays of equal length).

Return ONLY the JSON array. Do not include explanation or markdown.
"""

    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )

        response.raise_for_status()
        raw_output = response.json()["choices"][0]["message"]["content"]
        print("Raw Groq Output:\n", raw_output)
        return clean_json_response(raw_output)

    except Exception as e:
        print("Error querying Groq:", str(e))
        return "[]"
