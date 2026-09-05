import uuid
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException

from app.pdf_parser import extract_text_from_pdf
from app.file_validator import validate_pdf
from app.text_cleaner import clean_text
from app.llm_service import extract_medical_data
from app.rag_service import index_knowledge_base
from app.analysis_service import analyze_medical_data


app = FastAPI(
    title="AI Medical Report Analyzer",
    description="AI-powered medical report analysis API",
    version="1.0.0"
)


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
def root():

    return {
        "message": "AI Medical Report Analyzer API is running"
    }


@app.post("/upload")
async def upload_report(
    file: UploadFile = File(...)
):

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

        extracted_text = clean_text(
            extracted_text
        )

        if len(extracted_text.strip()) < 20:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Could not extract enough text "
                    "from this PDF. OCR may be required."
                )
            )

        medical_data = extract_medical_data(
            extracted_text
        )

        index_knowledge_base()

        analysis = analyze_medical_data(
            medical_data
        )

        return {

            "filename": file.filename,

            "medical_data": medical_data,

            "analysis": analysis

        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

    finally:

        file_path.unlink(
            missing_ok=True
        )