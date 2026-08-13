from pathlib import Path

ALLOWED_EXTENSIONS = {".pdf"}

MAX_FILE_SIZE = 10 * 1024 * 1024

def validate_pdf(filename: str, file_size: int):

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Only PDF files are allowed.")

    if file_size > MAX_FILE_SIZE:
        raise ValueError("File size must be less than 10MB.")

    if file_size == 0:
        raise ValueError("The uploaded file is empty.")

    return True