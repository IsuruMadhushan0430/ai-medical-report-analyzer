from app.rag_service import build_context
from app.llm_service import client
from google.genai import types


def analyze_medical_data(medical_data: dict) -> dict:

    tests = medical_data.get("tests", [])

    test_names = [
        test.get("name")
        for test in tests
        if test.get("name")
    ]

    query = (
        "Medical laboratory information about: "
        + ", ".join(test_names)
    )

    context = build_context(
        query=query,
        top_k=5
    )

    prompt = f"""
You are an educational medical report explanation assistant.

Analyze ONLY the information contained in the provided
medical data and retrieved reference context.

IMPORTANT:
- Do not diagnose the patient.
- Do not claim that an abnormal result proves a disease.
- Do not invent values.
- Do not invent reference ranges.
- Use the reference ranges from the report when available.
- Clearly distinguish reported facts from general information.
- If information is missing, say that it is unavailable.

Medical data:

{medical_data}

Retrieved medical reference context:

{context}

Return your response in this JSON structure:

{{
    "summary": "",
    "results": [
        {{
            "name": "",
            "value": null,
            "unit": "",
            "reference_range": "",
            "status": "",
            "explanation": ""
        }}
    ],
    "important_notes": [],
    "disclaimer": ""
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    response_text = response.text.strip()

    if response_text.startswith("```"):
        response_text = response_text.replace(
            "```json", ""
        )
        response_text = response_text.replace(
            "```", ""
        )
        response_text = response_text.strip()

    import json

    return json.loads(response_text)