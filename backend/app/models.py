import re
from typing import Optional

from pydantic import BaseModel, field_validator


class PatientInfo(BaseModel):

    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None

    @field_validator("age", mode="before")
    @classmethod
    def normalize_age(cls, value):
        if isinstance(value, str):
            match = re.search(r"\d+", value)
            if match:
                return int(match.group())
        return value


class MedicalTest(BaseModel):

    name: str
    value: Optional[float | str] = None
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    status: Optional[str] = "unknown"


class MedicalData(BaseModel):

    patient: PatientInfo
    tests: list[MedicalTest]
    report_date: Optional[str] = None


class AnalysisResult(BaseModel):

    name: str
    value: Optional[float | str] = None
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    status: Optional[str] = None
    explanation: Optional[str] = None


class MedicalAnalysis(BaseModel):

    summary: str
    results: list[AnalysisResult]
    important_notes: list[str]
    disclaimer: str


class UploadResponse(BaseModel):

    filename: str
    medical_data: MedicalData
    analysis: MedicalAnalysis