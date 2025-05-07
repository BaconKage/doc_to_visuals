
import fitz  # PyMuPDF
import pandas as pd
from docx import Document
import io

def extract_file_data(file):
    filename = file.filename.lower()

    if filename.endswith('.pdf'):
        doc = fitz.open(stream=file.read(), filetype='pdf')
        return "\n".join([page.get_text() for page in doc])

    elif filename.endswith('.csv'):
        df = pd.read_csv(file)
        return df.to_string()

    elif filename.endswith('.txt'):
        return file.read().decode('utf-8')

    elif filename.endswith('.docx'):
        doc = Document(io.BytesIO(file.read()))
        return "\n".join([para.text for para in doc.paragraphs])

    else:
        return "Unsupported file format."
