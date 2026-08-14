from app.rag_service import build_context
from app.llm_service import client

def analyze_medical_data(medical_data: dict):
    query_parts =[]
    for test in medical_data.get("tests", []):
        name = test.get("name")
        if name:
            query_parts.append(name)

        query = "Medical laboratory interpretation: " + ", ".join(
            query_parts
        )

        context = build_context(
            query,
            top_k=3
        )

        prompt = f"""
You are an educational medical report explanation assistant.
Use the provided laboratory information and retrieved reference context.
Do not diagnose the patient.
Do not claim that as abnormal result proves a disease.
Explain results clearly and cautiously.
Medical data:

{medical_data}

Retrieved reference context:

{context}

Provide:

1. Summary of the reported results
2. Results outside the provided reference ranges
3. General educational explanation
4. Important limitations
5.Suggestion to discuss concerning results with a qualified healthcare professional when appropriate
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text