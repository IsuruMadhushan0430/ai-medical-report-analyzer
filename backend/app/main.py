import uuid

from fastapi import (
    FastAPI,
    File,
    HTTPException,
    UploadFile
)

from fastapi.middleware.cors import CORSMiddleware

from app.analysis_service import analyze_medical_data
from app.config import UPLOAD_DIR
from app.file_validator import validate_pdf
from app.llm_service import extract_medical_data
from app.models import UploadResponse
from app.pdf_parser import extract_text_from_pdf
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

        validate_pdf(
            file.filename,
            len(contents)
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    safe_filename = (
        f"{uuid.uuid4()}.pdf"
    )

    file_path = (
        UPLOAD_DIR / safe_filename
    )

    try:

        with open(
            file_path,
            "wb"
        ) as buffer:

            buffer.write(contents)

        try:
            extracted_text = (
                extract_text_from_pdf(
                    str(file_path)
                )
            )
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

        extracted_text = clean_text(
            extracted_text
        )

        if len(extracted_text) < 20:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Could not extract enough "
                    "text from this PDF."
                )
            )

        try:
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
        except Exception as e:
            error_message = str(e)

            if "RESOURCE_EXHAUSTED" in error_message or "429" in error_message:
                raise HTTPException(
                    status_code=429,
                    detail=(
                        "The AI service quota has been exceeded. "
                        "Please wait and try again, or configure a Gemini API key "
                        "with available quota."
                    ),
                    headers={"Retry-After": "30"}
                )

            raise HTTPException(
                status_code=502,
                detail=f"AI analysis failed: {error_message}"
            )

        try:
            return UploadResponse(
                filename=file.filename,
                medical_data=medical_data,
                analysis=analysis
            )
        except Exception as e:
            raise HTTPException(
                status_code=502,
                detail=f"AI response did not match the expected format: {str(e)}"
            )

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

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "AI Medical Report Analyzer"
    }