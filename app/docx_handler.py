from docxtpl import DocxTemplate
from fastapi.responses import StreamingResponse
from io import BytesIO
import tempfile
from starlette.datastructures import UploadFile

async def process_docx(file: UploadFile, replacements: dict):
    # read the uploaded file bytes and grab its original filename
    docx_bytes = await file.read()
    input_filename = file.filename

    # drop into a temp file so docxtpl can load it
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
        tmp.write(docx_bytes)
        tmp.flush()
        tpl = DocxTemplate(tmp.name)
        tpl.render(replacements)

        # write out to an in‑memory buffer
        output_io = BytesIO()
        tpl.save(output_io)
        output_io.seek(0)

    # use the original filename in the Content-Disposition header
    headers = {
        "Content-Disposition": f'inline; filename="{input_filename}"'
    }

    return StreamingResponse(
        output_io,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers=headers
    )
