import fitz  # PyMuPDF
from fastapi.responses import StreamingResponse
from io import BytesIO

def process_pdf(pdf_bytes, replacements: dict):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    for page in doc:
        text_instances = []

        for key, value in replacements.items():
            search_term = f"${key}"
            found = page.search_for(search_term)
            for inst in found:
                text_instances.append((inst, value))

        for inst, replacement in text_instances:
            # Erase the original text by drawing a white rectangle over it
            page.draw_rect(inst, color=(1, 1, 1), fill=(1, 1, 1))
            # Insert the new replacement text at the same position
            page.insert_text(inst.tl, replacement, fontsize=12, fontname="helv")

    output_io = BytesIO()
    doc.save(output_io)
    doc.close()
    output_io.seek(0)

    return StreamingResponse(
        output_io,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=filled.pdf"},
    )
