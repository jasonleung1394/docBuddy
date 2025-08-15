from fastapi import FastAPI, UploadFile, File, Form
from app.pdf_handler import process_pdf
from app.docx_handler import process_docx
from app.extract_fields import extract_from_pdf, extract_from_docx
import json

app = FastAPI()

@app.post("/render/pdf")
async def render_pdf(
    file: UploadFile = File(...),
    data: str = Form(...)
):
    replacements = json.loads(data)
    return await process_pdf(file, replacements)

@app.post("/render/docx")
async def render_docx(
    file: UploadFile = File(...),
    data: str = Form(...)
):
    replacements = json.loads(data)
    return await process_docx(file, replacements)

@app.post("/extract/pdf")
async def extract_pdf(
    file: UploadFile = File(...),
    keywords: str = Form(...)
):
    keyword_list = json.loads(keywords)
    content = await file.read()
    result = extract_from_pdf(content, keyword_list)
    return result

@app.post("/extract/docx")
async def extract_docx(
    file: UploadFile = File(...),
    keywords: str = Form(...)
):
    keyword_list = json.loads(keywords)
    content = await file.read()
    result = extract_from_docx(content, keyword_list)
    return result
