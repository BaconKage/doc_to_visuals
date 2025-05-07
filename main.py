from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.file_parser import parse_file
from utils.groq_client import query_groq

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Doc Visualizer API is running."

@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files["file"]
        if not file:
            return jsonify({"error": "No file provided"}), 400

        content = parse_file(file)
        charts = query_groq(content)

        return jsonify({"charts": charts})  # ✅ JSON-safe dictionary return
    except Exception as e:
        print("Error during upload:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
