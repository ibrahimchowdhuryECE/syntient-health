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
    assert data["service"] == "retrieval"

def test_search_endpoint():
    """Test that the search endpoint returns stub response"""
    request_data = {
        "pathway": "cardiology",
        "query": "chest pain assessment"
    }
    
    response = client.post("/kb/search", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "hits" in data
    assert isinstance(data["hits"], list)
    assert len(data["hits"]) == 2
    
    # Check first hit
    first_hit = data["hits"][0]
    assert first_hit["id"] == "doc_001"
    assert first_hit["section"] == "assessment"
    assert "Chest pain assessment" in first_hit["snippet"]
