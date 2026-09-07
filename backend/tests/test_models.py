from app.models import UploadResponse


def test_upload_response_accepts_mixed_report_values():
    response = UploadResponse(
        filename="report.pdf",
        medical_data={
            "patient": {"name": "Patient", "age": "45 years"},
            "tests": [
                {"name": "Hemoglobin", "value": 13.5},
                {"name": "Urine color", "value": "Pale Yellow"},
                {"name": "Protein", "value": "Negative"},
            ],
        },
        analysis={
            "summary": "Mixed results",
            "results": [
                {"name": "Urine color", "value": "Pale Yellow"},
                {"name": "Hemoglobin", "value": 13.5},
            ],
            "important_notes": [],
            "disclaimer": "Educational information only.",
        },
    )

    assert response.medical_data.patient.age == 45
    assert response.medical_data.tests[0].value == 13.5
    assert response.medical_data.tests[1].value == "Pale Yellow"
    assert response.analysis.results[0].value == "Pale Yellow"