import pytesseract
from PIL import Image, ImageEnhance, ImageFilter


def extract_text_from_image(file_path: str) -> str:
    image = Image.open(file_path)

    image = image.convert("L")

    image = ImageEnhance.Contrast(image).enhance(2)

    image = image.filter(ImageFilter.SHARPEN)

    text = pytesseract.image_to_string(image)

    return text