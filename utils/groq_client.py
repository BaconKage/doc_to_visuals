import requests
import os
import re
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

Do NOT include any explanation or extra text — only the JSON array.
"""

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a data visualization expert."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        raw_output = res.json()["choices"][0]["message"]["content"]
        return clean_json_response(raw_output)
    except Exception as e:
        return f"[{{\"type\": \"error\", \"title\": \"Groq Error\", \"x\": [], \"y\": [], \"error\": \"{str(e)}\"}}]"
