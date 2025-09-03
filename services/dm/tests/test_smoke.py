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
    assert data["service"] == "dm"

def test_evaluate_endpoint():
    """Test that the evaluate endpoint returns stub response"""
    request_data = {
        "policy": {
            "confidence_threshold": 0.7
        },
        "evidence": {
            "patient_id": "patient_789",
            "presenting_complaint": "chest pain",
            "fields": {
                "age": 45,
                "gender": "M"
            },
            "free_text": "Chest pain started 2 hours ago"
        }
    }
    
    response = client.post("/dm/evaluate", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["decision_ready"] is True
    assert data["mts_category"] == "very_urgent"
    assert data["confidence"] == 0.78
    assert isinstance(data["followups"], list)
    assert data["immediate_flag"] is False
