from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.file_parser import parse_file
from utils.groq_client import query_groq
import json

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "Doc to Visuals backend is running."

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    try:
        # Step 1: Extract content
        content = parse_file(file)

        # Step 2: Send to Groq
        groq_output = query_groq(content)

        # Step 3: Parse JSON string into Python list
        try:
            chart_data = json.loads(groq_output)
        except json.JSONDecodeError:
            chart_data = []

        # Step 4: Return raw chart data
        return jsonify({"charts": chart_data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
