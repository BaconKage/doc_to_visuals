import requests
import os
from dotenv import load_dotenv

load_dotenv()

def query_groq(text):
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a data visualization expert."},
            {"role": "user", "content": f"Analyze this:\n{text}\n\nSuggest up to 3 charts in JSON format with type, title, x and y arrays."}
        ]
    }
    res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    return res.json()["choices"][0]["message"]["content"]
