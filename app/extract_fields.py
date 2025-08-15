import re
import fitz  # PyMuPDF
from docx import Document
from io import BytesIO


def extract_fields_from_text(text, keywords):
    results = {}

    for key in keywords:
        # Build a regex to match key and extract next phrase
        # e.g., first name: Jason or First Name - Jason Leung
        pattern = re.compile(rf"{re.escape(key)}\s*[:\-–]?\s*([^\n,;]+)", re.IGNORECASE)
        match = pattern.search(text)
        if match:
            results[key] = match.group(1).strip()
        else:
            results[key] = None

    return results


def extract_from_pdf(pdf_bytes, keywords):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    full_text = "\n".join([page.get_text() for page in doc])
    doc.close()
    return extract_fields_from_text(full_text, keywords)


def extract_from_docx(docx_bytes, keywords):
    buffer = BytesIO(docx_bytes)
    doc = Document(buffer)
    full_text = "\n".join([para.text for para in doc.paragraphs])
    return extract_fields_from_text(full_text, keywords)
