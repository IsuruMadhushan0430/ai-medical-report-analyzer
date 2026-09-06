import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured."
    )


UPLOAD_DIR = BASE_DIR / "backend" / "uploads"

KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"

CHROMA_DIR = BASE_DIR / "chroma_db"


MAX_FILE_SIZE = 10 * 1024 * 1024