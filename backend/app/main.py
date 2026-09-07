import json
import uuid
from pathlib import Path
from fastapi import (
    FastAPI,
    File,
    HTTPException,
    UploadFile
)

from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from app.analysis_service import analyze_medical_data
from app.config import UPLOAD_DIR
from app.file_validator import validate_medical_file
from app.llm_service import extract_medical_data
from app.models import UploadResponse
from app.pdf_parser import extract_text_from_pdf
from app.image_parser import extract_text_from_image
from app.rag_service import initialize_rag
from app.text_cleaner import clean_text


app = FastAPI(
    title="AI Medical Report Analyzer",
    description=(
        "AI-powered medical report analysis "
        "using RAG and LLMs."
    ),
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

@app.on_event("startup")
def startup_event():

    initialize_rag()

@app.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_report(
    file: UploadFile = File(...)
):

    contents = await file.read()

    try:

        validate_medical_file(
            file.filename,
            len(contents)
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    extension = Path(file.filename).suffix.lower()

    safe_filename = f"{uuid.uuid4()}{extension}"
    file_path = UPLOAD_DIR / safe_filename

    try:

        with open(
            file_path,
            "wb"
        ) as buffer:

            buffer.write(contents)

        if extension == ".pdf":
            extracted_text = (
                            extract_text_from_pdf(
                                str(file_path)
                            )
                        )

        elif extension in {".jpg", ".jpeg", ".png"}:
            extracted_text = (
                            extract_text_from_image(
                                str(file_path)
                            )
                        )

        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type."
            )

        extracted_text = clean_text(
            extracted_text
        )

        if len(extracted_text) < 20:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Could not extract enough text from the report. "
                    "Please upload a clearer PDF or image."
                )
            )

        medical_data = (
             extract_medical_data(
                extracted_text
            )
        )

        analysis = (
             analyze_medical_data(
                medical_data
            )
        )

        return {
            "filename": file.filename,
            "medical_data": medical_data,
            "analysis": analysis
        }

    except HTTPException:
        raise

    except (json.JSONDecodeError, ValidationError) as e:
        raise HTTPException(
            status_code=502,
            detail=(
                "The AI service returned an invalid response. "
                f"Please try again. Details: {str(e)}"
            )
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

    finally:
        file_path.unlink(missing_ok=True)

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "AI Medical Report Analyzer"
    }