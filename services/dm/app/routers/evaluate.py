from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

router = APIRouter()

class EvaluationPolicy(BaseModel):
    confidence_threshold: float

class PatientEvidence(BaseModel):
    patient_id: str
    presenting_complaint: str
    fields: Dict[str, Any]
    free_text: Optional[str] = None

class EvaluateRequest(BaseModel):
    policy: EvaluationPolicy
    evidence: PatientEvidence

class EvaluateResponse(BaseModel):
    decision_ready: bool
    mts_category: str
    confidence: float
    followups: List[str]
    immediate_flag: bool

@router.post("/evaluate", response_model=EvaluateResponse)
async def evaluate_complaint(request: EvaluateRequest):
    """
    Evaluate patient complaint for urgency and triage.
    Returns stub response for development.
    """
    # Stub implementation - returns static response
    # TODO: Implement actual triage logic
    
    return EvaluateResponse(
        decision_ready=True,
        mts_category="very_urgent",
        confidence=0.78,
        followups=[],
        immediate_flag=False
    )
