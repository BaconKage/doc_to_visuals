from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from utils.file_parser import extract_text
from utils.groq_client import query_groq
from utils.chart_builder import build_charts
import uvicorn

app = FastAPI()

# Enable CORS for local dev and frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        text = extract_text(contents, file.filename)
        chart_json = query_groq(text)
        charts = build_charts(chart_json)
        return {"charts": charts}
    except Exception as e:
        print("Upload Error:", str(e))
        return {"error": "Invalid response from server"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
