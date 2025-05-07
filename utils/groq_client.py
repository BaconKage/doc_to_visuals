import requests
import os
from dotenv import load_dotenv

load_dotenv()

def query_groq(text):
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }

    prompt = f"""You are a data visualization expert.

Given this content:

{text}

Return ONLY a valid JSON array of up to 3 charts.
Each chart should be a JSON object like:
{{
  "type": "bar" | "line" | "pie",
  "title": "Chart Title",
  "x": ["Label1", "Label2", ...],
  "y": [Value1, Value2, ...]
}}

⚠️ Do NOT include any explanation or extra text — only return the raw JSON array itself.
"""

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )
        content = response.json()["choices"][0]["message"]["content"]
        print("Raw Groq Chart Output:\n", content)  # For debugging
        return content  # returning as JSON string
    except Exception as e:
        print("Error from Groq:", e)
        return "[]"
