from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class AskRequest(BaseModel):
    followups: List[str]
    locale: Optional[str] = "en-US"

class AskResponse(BaseModel):
    prompt: str
    expected_field: str

@router.post("/ask", response_model=AskResponse)
async def generate_follow_up(request: AskRequest):
    """
    Generate follow-up questions or messages.
    Returns stub response for development.
    """
    # Stub implementation - returns static response
    # TODO: Implement actual question generation logic
    
    return AskResponse(
        prompt="How long has the chest pain been present?",
        expected_field="duration"
    )
