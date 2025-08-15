import os, tempfile
from fastapi.responses import FileResponse
from docxtpl import DocxTemplate

async def process_docx(file, replacements: dict):
    # Save upload to a temp file
    in_tmp = tempfile.NamedTemporaryFile(suffix=".docx", delete=False)
    try:
        in_bytes = await file.read()
        in_tmp.write(in_bytes)
        in_tmp.flush()
        in_tmp.close()  # important on Windows before opening with DocxTemplate

        # Render to another temp file on disk (easier to debug than BytesIO)
        out_path = tempfile.mktemp(suffix=".docx")
        tpl = DocxTemplate(in_tmp.name)
        tpl.render(replacements)
        tpl.save(out_path)

        # Return as a real file so you can download and open it
        return FileResponse(
            out_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=file.filename or "output.docx",
        )
    finally:
        try: os.unlink(in_tmp.name)
        except OSError: pass
