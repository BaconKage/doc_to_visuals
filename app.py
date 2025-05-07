
from flask import Flask, render_template, request
from utils.file_parser import extract_file_data
from utils.groq_client import query_groq
from utils.chart_builder import build_charts

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file:
            content = extract_file_data(uploaded_file)
            response = query_groq(content)
            charts = build_charts(response)
            return render_template('result.html', charts=charts)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
