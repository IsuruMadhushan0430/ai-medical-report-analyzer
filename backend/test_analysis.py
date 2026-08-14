from app.rag_service import index_knowledge_base
from app.analysis_service import analyze_medical_data

index_knowledge_base()

sample_data = {
    "patient": {
        "name":None,
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

result = analyze_medical_data(
    sample_data
)

print(result)