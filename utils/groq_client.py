import requests
import os
import re
import json
from dotenv import load_dotenv

load_dotenv()

def clean_json_response(raw_text):
    """
    Extracts the first JSON array from the LLM output using regex.
    """
    match = re.search(r"\[.*\]", raw_text, re.DOTALL)
    return match.group(0) if match else "[]"

def query_groq(text):
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }

    prompt = f"""Given this content:

{text}

Return ONLY a raw JSON array of up to 3 charts.
Each chart must be an object like:
{{
  "type": "bar" | "line" | "pie",
  "title": "...",
  "x": [...],
  "y": [...]
}}
Ensure x-axis values are valid strings (e.g., years or categories).
"""

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
    raw_output = response.json()["choices"][0]["message"]["content"]

    print("Raw Groq Output:\n", raw_output)

    try:
        parsed_charts = json.loads(clean_json_response(raw_output))

        # ✅ Ensure all x values are stringified
        for chart in parsed_charts:
            chart["x"] = list(map(str, chart.get("x", [])))
            chart["y"] = chart.get("y", [])

        return parsed_charts

    except Exception as e:
        print("Groq parse error:", str(e))
        return []
