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
    assert data["service"] == "mam"

def test_ask_endpoint():
    """Test that the ask endpoint returns stub response"""
    request_data = {
        "followups": ["duration", "severity"],
        "locale": "en-US"
    }
    
    response = client.post("/mam/ask", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["prompt"] == "How long has the chest pain been present?"
    assert data["expected_field"] == "duration"
