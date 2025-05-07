import os
import io
import csv
import fitz  # PyMuPDF
import pdfplumber
import pandas as pd
from docx import Document

def parse_file(file):
    filename = file.filename
    extension = os.path.splitext(filename)[1].lower()

    if extension == ".csv":
        return file.read().decode("utf-8")

    elif extension == ".txt":
        return file.read().decode("utf-8")

    elif extension == ".pdf":
        return extract_pdf_tables(file)

    elif extension == ".docx":
        return extract_docx_text(file)

    else:
        return "Unsupported file type."

def extract_docx_text(file):
    content = ""
    doc = Document(file)
    for para in doc.paragraphs:
        content += para.text + "\n"
    return content

def extract_pdf_tables(file):
    content = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if row:
                        clean_row = [cell.strip() if cell else "" for cell in row]
                        content += ", ".join(clean_row) + "\n"
    return content
