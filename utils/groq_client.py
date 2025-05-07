import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

def clean_json_response(raw_text):
    match = re.search(r'\[.*\]', raw_text, re.DOTALL)
    return match.group(0) if match else "[]"

def query_groq(text):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("GROQ_API_KEY not found in environment.")
        return "[]"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    messages = [
        {
            "role": "user",
            "content": (
                f"Given this content:\n\n{text}\n\n"
                "Return up to 5 charts as a raw JSON array. Each chart should follow:\n"
                '{\n"type": "bar" | "line" | "pie",\n"title": "...",\n"x": [...],\n"y": [...]\n}\n\n'
                "Guidelines:\n"
                "- Use 'line' or 'bar' for time-series like Revenue, ARPU, Subscribers.\n"
                "- Use 'pie' only for breakdowns (e.g., Expense split).\n"
                "- Return ONLY the JSON array. No extra text or markdown."
            )
        }
    ]

    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 1024,
        "stop": []

    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        raw_text = result["choices"][0]["message"]["content"]
        print("Raw Groq Output:\n", raw_text)
        return clean_json_response(raw_text)

    except requests.exceptions.RequestException as e:
        print("Error querying Groq:", str(e))
        return "[]"
