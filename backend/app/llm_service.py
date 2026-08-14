import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not configured")

client = genai.Client(api_key=api_key)

def extract_medical_data(report_text: str) -> dict:

    prompt = f"""
You are a medical report information extraction system.

Your task is ONLY to extract information explicitly present
in the provided medical report.

Do not diagnose the patient.
Do not invent missing values.
Do not assume information that is not present.

Return valid JSON with this structure:

{{
    "patient": {{
        "name": null,
        "age": null,
        "gender": null
    }},
    "tests": [
        {{
            "name": "",
            "value": null,
            "unit": "",
            "reference_range": "",
            "status": "unknown"
        }}
    ],
    "report_date": null
}}

Medical report:

{report_text}
"""

    response  = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    response_text = response.text.strip()

    if response_text.startswith("```"):
        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

    return json.loads(response_text)