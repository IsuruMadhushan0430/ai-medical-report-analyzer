import pytest

from app.file_validator import validate_pdf

def test_valid_pdf():

    assert validate_pdf(
        "report.pdf",
        1024
    ) is True

def test_invalid_extension():

    with pytest.raises(ValueError):  
        validate_pdf(
            "report.jpg",
            1024
        )

def test_file_too_large():

    with pytest.raises(ValueError):
        validate_pdf(
            "report.pdf",
            11*1024*1024
        )

def test_empty_file():

    with pytest.raises(ValueError):
        validate_pdf(
            "report.pdf",
            0
        )