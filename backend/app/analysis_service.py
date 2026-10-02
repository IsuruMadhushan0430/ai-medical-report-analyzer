import json
from google import genai

from app.config import GEMINI_API_KEY
from app.rag_service import build_context


client = genai.Client(api_key=GEMINI_API_KEY)


def analyze_medical_data(medical_data: dict, language: str = "en"):

    test_names = [
        test.get("name", "")
        for test in medical_data.get("tests", [])
        if test.get("name")
    ]

    query = " ".join(test_names)

    context = build_context(query, 3)

    if language == "si":
        language_instruction = """
Generate the summary, explanations, important notes, and disclaimer
in Sinhala language.

Use clear, simple Sinhala that an ordinary patient can understand.

Keep medical test names, abbreviations, units, numerical values,
and reference ranges unchanged where appropriate.

Do not translate numerical values.
Do not invent medical information.
Do not provide a diagnosis.
"""
    else:
        language_instruction = """
Generate the summary, explanations, important notes, and disclaimer
in English.

Use clear language that an ordinary patient can understand.

Do not invent medical information.
Do not provide a diagnosis.
"""

    prompt = f"""
You are a medical report explanation assistant.

Your task is to explain the provided medical test results
using the supplied medical knowledge.

IMPORTANT:
- Do not diagnose the patient.
- Do not invent missing values.
- Do not change numerical test values.
- Do not change units.
- Clearly distinguish abnormal results from normal results.
- The explanation is educational only.

{language_instruction}

MEDICAL DATA:
{json.dumps(medical_data, indent=2)}

RELEVANT MEDICAL KNOWLEDGE:
{context}

Return ONLY valid JSON using this structure:

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
        contents=prompt
    )

    response_text = response.text.strip()

    if response_text.startswith("```"):
        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

    return json.loads(response_text)