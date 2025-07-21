from fastapi import FastAPI, UploadFile, File, Form
from app.pdf_handler import process_pdf
from app.docx_handler import process_docx
import json

app = FastAPI()

@app.post("/render/pdf")
async def render_pdf(
    file: UploadFile = File(...),
    data: str       = Form(...)
):
    replacements = json.loads(data)
    # pass the UploadFile and await the coroutine
    return await process_pdf(file, replacements)


@app.post("/render/docx")
async def render_docx(
    file: UploadFile = File(...),
    data: str       = Form(...)
):
    replacements = json.loads(data)
    return await process_docx(file, replacements)
