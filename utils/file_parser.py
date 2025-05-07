import os
import pdfplumber
from docx import Document
import re
import spacy

nlp = spacy.load("en_core_web_sm")

def parse_file(file):
    filename = file.filename
    extension = os.path.splitext(filename)[1].lower()

    if extension == ".csv":
        return file.read().decode("utf-8")

    elif extension == ".txt":
        return file.read().decode("utf-8")

    elif extension == ".pdf":
        text = extract_pdf_tables(file)
        if not text.strip() and os.getenv("ENABLE_NLP_FALLBACK") == "true":
            return extract_nlp_from_pdf(file)
        return text

    elif extension == ".docx":
        text = extract_docx_text(file)
        if os.getenv("ENABLE_NLP_FALLBACK") == "true":
            return convert_nlp_to_table(extract_nlp_from_text(text))
        return text

    else:
        return "Unsupported file type."


def extract_pdf_tables(file):
    content = ""
    with pdfplumber.open(file) as pdf:
        for i, page in enumerate(pdf.pages[:10]):  # Limit to first 10 pages
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if row:
                        clean_row = [cell.strip() if cell else "" for cell in row]
                        content += ", ".join(clean_row) + "\n"
    return content

def extract_docx_text(file):
    content = ""
    doc = Document(file)
    for para in doc.paragraphs:
        content += para.text + "\n"
    return content

def extract_nlp_from_pdf(file):
    content = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages[:5]:
            content += page.extract_text() + "\n"
    return convert_nlp_to_table(extract_nlp_from_text(content))

def extract_nlp_from_text(text):
    doc = nlp(text)
    financial_data = []
    year_pattern = re.compile(r"(19|20)\d{2}")
    money_pattern = re.compile(r"(₹|\$)?\s?[\d,.]+(?:\s?crores?)?")
    label_keywords = ["revenue", "profit", "loss", "capex", "ebitda", "income", "expense"]

    sentences = [sent.text.lower() for sent in doc.sents]

    for sentence in sentences:
        year_match = year_pattern.search(sentence)
        money_match = money_pattern.findall(sentence)
        matched_keywords = [kw for kw in label_keywords if kw in sentence]

        if year_match and money_match and matched_keywords:
            row = {
                "year": year_match.group(),
                "value": money_match[0].replace("₹", "").replace(",", "").strip(),
                "label": matched_keywords[0]
            }
            financial_data.append(row)

    return financial_data

def convert_nlp_to_table(data):
    table = "Year,Label,Value\n"
    for item in data:
        table += f"{item['year']},{item['label']},{item['value']}\n"
    return table
