import json
from types import SimpleNamespace

from app.analysis_service import analyze_medical_data


SAMPLE_DATA = {
    "patient": {
        "name": None,
        "age": 30,
        "gender": "Male"
    },
    "tests": [
        {
            "name": "Hemoglobin",
            "value": 12.1,
            "unit": "g/dL",
            "reference_range": "13.0 - 17.0",
            "status": "below_range"
        },
        {
            "name": "WBC",
            "value": 7.5,
            "unit": "x10^9/L",
            "reference_range": "4.0 - 11.0",
            "status": "normal"
        }
    ],
    "report_date": None
}


def test_analyze_medical_data(monkeypatch):
    expected_analysis = {
        "summary": "Two laboratory results were analyzed.",
        "results": [
            {
                "name": "Hemoglobin",
                "value": 12.1,
                "unit": "g/dL",
                "reference_range": "13.0 - 17.0",
                "status": "below_range",
                "explanation": "Below the supplied reference range."
            },
            {
                "name": "WBC",
                "value": 7.5,
                "unit": "x10^9/L",
                "reference_range": "4.0 - 11.0",
                "status": "normal",
                "explanation": "Within the supplied reference range."
            }
        ],
        "important_notes": [],
        "disclaimer": "Educational information only."
    }

    monkeypatch.setattr(
        "app.analysis_service.build_context",
        lambda query, top_k: "Reference context"
    )
    monkeypatch.setattr(
        "app.analysis_service.client.models.generate_content",
        lambda **kwargs: SimpleNamespace(
            text=json.dumps(expected_analysis)
        )
    )

    result = analyze_medical_data(SAMPLE_DATA)

    assert result == expected_analysis