from typing import Optional

from pydantic import BaseModel


class PatientInfo(BaseModel):

    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None


class MedicalTest(BaseModel):

    name: str
    value: Optional[float] = None
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    status: Optional[str] = "unknown"


class MedicalData(BaseModel):

    patient: PatientInfo
    tests: list[MedicalTest]
    report_date: Optional[str] = None


class AnalysisResult(BaseModel):

    name: str
    value: Optional[float] = None
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