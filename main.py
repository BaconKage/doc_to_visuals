from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.file_parser import parse_file
from utils.chart_builder import build_charts
from utils.groq_client import query_groq
import json

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        text = parse_file(file)
        llm_response = query_groq(text)
        charts_json = build_charts(llm_response)

        try:
            parsed_charts = json.loads(charts_json)
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON from LLM'}), 500

        return jsonify(parsed_charts)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "Doc Visualizer API Running"

app.run(debug=False, host="0.0.0.0", port=10000)
