import fitz  # PyMuPDF
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from io import BytesIO

async def process_pdf(file: UploadFile, replacements: dict):
    # Read the uploaded bytes and capture the original filename
    pdf_bytes = await file.read()
    input_filename = file.filename

    # Open in-memory PDF
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    # Do your find‑and‑replace
    for page in doc:
        text_instances = []
        for key, value in replacements.items():
            search_term = f"${key}"
            for inst in page.search_for(search_term):
                text_instances.append((inst, value))

        for inst, replacement in text_instances:
            # White‑out the old text and stamp new text
            page.draw_rect(inst, color=(1, 1, 1), fill=(1, 1, 1))
            page.insert_text(inst.tl, replacement, fontsize=12, fontname="helv")

    # Write out to a buffer
    output_io = BytesIO()
    doc.save(output_io)
    doc.close()
    output_io.seek(0)

    # Return with the original filename
    headers = {
        "Content-Disposition": f'inline; filename="{input_filename}"'
    }
    return StreamingResponse(
        output_io,
        media_type="application/pdf",
        headers=headers
    )
