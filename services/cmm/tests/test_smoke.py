import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test that the health endpoint returns 200"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["service"] == "cmm"

def test_propose_endpoint():
    """Test that the propose endpoint returns stub response"""
    request_data = {
        "patient_id": "patient_789",
        "mts_category": "urgent",
        "window": "same_day",
        "constraints": {
            "preferred_time": "morning",
            "preferred_provider": "dr_smith"
        }
    }
    
    response = client.post("/cmm/propose", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "proposals" in data
    assert isinstance(data["proposals"], list)
    assert len(data["proposals"]) == 2
    assert data["fallback"] == "NONE"
    
    # Check first proposal
    first_proposal = data["proposals"][0]
    assert first_proposal["slot_id"] == "slot_001"
    assert first_proposal["start"] == "2024-01-15T10:00:00Z"
    assert first_proposal["provider"] == "dr_smith"
