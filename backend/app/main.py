import uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException

from app.pdf_parser import extract_text_from_pdf
from app.file_validator import validate_pdf

app = FastAPI(
    title="AI Medical Report Analyzer",
    description="API for analyzing medical reports",
    version="1.0.0"
)

UPLOAD_DIR  = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
def root():
    return{
        "message": "AI Medical Report Analyzer API is running"
    }

@app.post("/upload")
async def upload_report(file: UploadFile = File(...)):

    contents = await file.read()

    try:
        validate_pdf(
            file.filename,
            len(contents)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    safe_filename = f"{uuid.uuid4()}.pdf"

    file_path = UPLOAD_DIR / safe_filename

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    try:
        extracted_text = extract_text_from_pdf(
            str(file_path)
        )
    except ValueError as e:
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return {
        "filename": file.filename,
        "text_length": len(extracted_text),
        "text": extracted_text
    }