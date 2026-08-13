from pathlib import Path
from pypdf import PdfReader

def extract_text_from_pdf(file_path: str) -> str:

    try:
        reader = PdfReader(file_path)

        extracted_text = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()

            if text:
                extracted_text.append(
                    f"\n--- Page {page_number} ---\n{text}"
                )

        return "\n".join(extracted_text).strip()

    except Exception as e:
        raise ValueError(f"Could not read PDF: {str(e)}")