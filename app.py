from flask import Flask, request, jsonify
from utils.file_parser import extract_file_data
from utils.groq_client import query_groq
from utils.chart_builder import build_charts

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from Bolt

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Step 1: Extract content
        content = extract_file_data(uploaded_file)

        # Step 2: Send to Groq and get chart suggestions
        groq_response = query_groq(content)

        # Step 3: Build Plotly charts as HTML strings
        charts = build_charts(groq_response)

        return jsonify({"charts": charts}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Doc-to-Viz API. POST a file to /upload"}), 200

if __name__ == '__main__':
    app.run(debug=True)
