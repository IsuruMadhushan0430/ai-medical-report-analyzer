import pytest

from app.file_validator import validate_medical_file

def test_valid_pdf():

    assert validate_medical_file(
        "report.pdf",
        1024
    ) is True

def test_valid_jpg():

    assert validate_medical_file(
        "report.jpg",
        1024
    ) is True

def test_valid_png():

    assert validate_medical_file(
        "report.png",
        1024
    ) is True

def test_valid_jpeg():

    assert validate_medical_file(
        "report.jpeg",
        1024
    ) is True

def test_invalid_extension():

    with pytest.raises(ValueError):  
        validate_medical_file(
            "report.docx",
            1024
        )

def test_file_too_large():

    with pytest.raises(ValueError):
        validate_medical_file(
            "report.pdf",
            11*1024*1024
        )

def test_empty_file():

    with pytest.raises(ValueError):
        validate_medical_file(
            "report.pdf",
            0
        )