from pathlib import Path
from app.config import MAX_FILE_SIZE


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png"
}


def validate_medical_file(filename: str, file_size: int):
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Only PDF, JPG, JPEG, and PNG files are allowed."
        )

    if file_size <= 0:
        raise ValueError("The uploaded file is empty.")

    if file_size > MAX_FILE_SIZE:
        raise ValueError("File size must be less than 10 MB.")

    return True