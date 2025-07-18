from fastapi import FastAPI, UploadFile, File, Form
from app.pdf_handler import process_pdf
from app.docx_handler import process_docx
import json

app = FastAPI()

@app.post("/render/pdf")
async def render_pdf(file: UploadFile = File(...), data: str = Form(...)):
    replacements = json.loads(data)
    content = await file.read()
    output = process_pdf(content, replacements)
    return output

@app.post("/render/docx")
async def render_docx(file: UploadFile = File(...), data: str = Form(...)):
    replacements = json.loads(data)
    content = await file.read()
    output = process_docx(content, replacements)
    return output
