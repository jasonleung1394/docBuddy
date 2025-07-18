from docxtpl import DocxTemplate
from fastapi.responses import StreamingResponse
from io import BytesIO
import tempfile

def process_docx(docx_bytes, replacements: dict):
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
        tmp.write(docx_bytes)
        tmp.flush()
        tpl = DocxTemplate(tmp.name)
        tpl.render(replacements)

        output_io = BytesIO()
        tpl.save(output_io)
        output_io.seek(0)

    return StreamingResponse(output_io, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", headers={"Content-Disposition": "inline; filename=filled.docx"})
