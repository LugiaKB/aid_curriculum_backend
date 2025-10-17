"""
Basic tests for the AI Resume Builder API.

Run with: pytest tests/
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns correct information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["version"] == "1.0.0"


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "api_version" in data


def test_create_resume():
    """Test creating a resume."""
    resume_data = {
        "full_name": "Test User",
        "professional_title": "Software Developer",
        "contact": {
            "email": "test@example.com",
            "phone": "+1234567890"
        },
        "education": [],
        "experience": [],
        "projects": [],
        "skills": []
    }
    
    response = client.post("/api/resumes/", json=resume_data)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["full_name"] == "Test User"


def test_list_resumes():
    """Test listing resumes."""
    response = client.get("/api/resumes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_generate_resume_content():
    """Test AI resume generation."""
    request_data = {
        "job_description": "Python developer position with FastAPI experience",
        "experience_level": "mid-level"
    }
    
    response = client.post("/api/resumes/generate", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "generated_content" in data
    assert "suggestions" in data


def test_analyze_resume():
    """Test resume analysis."""
    request_data = {
        "resume_content": "Test resume content with some professional experience"
    }
    
    response = client.post("/api/resumes/analyze", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert "strengths" in data
    assert "improvements" in data
    assert "suggestions" in data
    assert 0 <= data["score"] <= 100


def test_get_nonexistent_resume():
    """Test getting a resume that doesn't exist."""
    response = client.get("/api/resumes/nonexistent-id")
    assert response.status_code == 404


def test_update_nonexistent_resume():
    """Test updating a resume that doesn't exist."""
    resume_data = {
        "full_name": "Updated User",
        "contact": {
            "email": "updated@example.com"
        }
    }
    
    response = client.put("/api/resumes/nonexistent-id", json=resume_data)
    assert response.status_code == 404


def test_delete_nonexistent_resume():
    """Test deleting a resume that doesn't exist."""
    response = client.delete("/api/resumes/nonexistent-id")
    assert response.status_code == 404
