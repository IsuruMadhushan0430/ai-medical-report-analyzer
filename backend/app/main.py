from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path

from app.pdf_parser import extract_text_from_pdf

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

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    file_path = UPLOAD_DIR / file.filename

    contents = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    extracted_text = extract_text_from_pdf(str(file_path))

    return {
        "filename": file.filename,
        "text": extracted_text
    }