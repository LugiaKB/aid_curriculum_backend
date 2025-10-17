import pytest
from fastapi.testclient import TestClient
from app.main import app, resumes_store


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_resumes_store():
    """Clear the resumes store before each test"""
    resumes_store.clear()
    yield
    resumes_store.clear()


def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "endpoints" in data


def test_create_resume(client):
    """Test creating a new resume"""
    resume_data = {
        "full_name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "location": "New York, NY",
        "summary": "Experienced software engineer",
        "skills": ["Python", "FastAPI", "PostgreSQL"],
        "experience": [
            {
                "company": "Tech Corp",
                "position": "Software Engineer",
                "location": "New York, NY",
                "start_date": "2020-01-01",
                "description": "Developed web applications",
                "is_current": True
            }
        ],
        "education": [
            {
                "institution": "University of Example",
                "degree": "Bachelor of Science",
                "field_of_study": "Computer Science",
                "start_date": "2016-09-01",
                "end_date": "2020-05-01",
                "gpa": "3.8"
            }
        ]
    }
    
    response = client.post("/resume", json=resume_data)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert "message" in data
    assert data["data"]["full_name"] == "John Doe"
    assert data["data"]["email"] == "john.doe@example.com"


def test_create_resume_minimal(client):
    """Test creating a resume with only required fields"""
    resume_data = {
        "full_name": "Jane Smith",
        "email": "jane.smith@example.com"
    }
    
    response = client.post("/resume", json=resume_data)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["full_name"] == "Jane Smith"


def test_create_resume_invalid_email(client):
    """Test creating a resume with invalid email"""
    resume_data = {
        "full_name": "Invalid User",
        "email": "not-an-email"
    }
    
    response = client.post("/resume", json=resume_data)
    assert response.status_code == 422  # Validation error


def test_get_resume(client):
    """Test retrieving a resume by ID"""
    # First create a resume
    resume_data = {
        "full_name": "Test User",
        "email": "test@example.com"
    }
    
    create_response = client.post("/resume", json=resume_data)
    assert create_response.status_code == 201
    
    # Extract resume ID from the message
    message = create_response.json()["message"]
    resume_id = message.split("ID: ")[1]
    
    # Now retrieve it
    get_response = client.get(f"/resume/{resume_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["status"] == "success"
    assert data["data"]["full_name"] == "Test User"


def test_get_nonexistent_resume(client):
    """Test retrieving a resume that doesn't exist"""
    response = client.get("/resume/nonexistent-id")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_update_resume(client):
    """Test updating an existing resume"""
    # First create a resume
    resume_data = {
        "full_name": "Original Name",
        "email": "original@example.com"
    }
    
    create_response = client.post("/resume", json=resume_data)
    message = create_response.json()["message"]
    resume_id = message.split("ID: ")[1]
    
    # Update the resume
    updated_data = {
        "full_name": "Updated Name",
        "email": "updated@example.com",
        "phone": "+9876543210"
    }
    
    update_response = client.put(f"/resume/{resume_id}", json=updated_data)
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["status"] == "success"
    assert data["data"]["full_name"] == "Updated Name"
    assert data["data"]["phone"] == "+9876543210"


def test_update_nonexistent_resume(client):
    """Test updating a resume that doesn't exist"""
    resume_data = {
        "full_name": "Test User",
        "email": "test@example.com"
    }
    
    response = client.put("/resume/nonexistent-id", json=resume_data)
    assert response.status_code == 404


def test_delete_resume(client):
    """Test deleting a resume"""
    # First create a resume
    resume_data = {
        "full_name": "To Be Deleted",
        "email": "delete@example.com"
    }
    
    create_response = client.post("/resume", json=resume_data)
    message = create_response.json()["message"]
    resume_id = message.split("ID: ")[1]
    
    # Delete the resume
    delete_response = client.delete(f"/resume/{resume_id}")
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert data["status"] == "success"
    
    # Verify it's deleted
    get_response = client.get(f"/resume/{resume_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_resume(client):
    """Test deleting a resume that doesn't exist"""
    response = client.delete("/resume/nonexistent-id")
    assert response.status_code == 404


def test_list_resumes(client):
    """Test listing all resumes"""
    # Initially should be empty
    response = client.get("/resumes")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    assert len(data["resume_ids"]) == 0
    
    # Create a couple of resumes
    client.post("/resume", json={"full_name": "User 1", "email": "user1@example.com"})
    client.post("/resume", json={"full_name": "User 2", "email": "user2@example.com"})
    
    # Now list should have 2 resumes
    response = client.get("/resumes")
    data = response.json()
    assert data["count"] == 2
    assert len(data["resume_ids"]) == 2


def test_resume_with_projects(client):
    """Test creating a resume with projects"""
    resume_data = {
        "full_name": "Project Developer",
        "email": "dev@example.com",
        "projects": [
            {
                "name": "E-commerce Platform",
                "description": "Built a scalable e-commerce platform",
                "technologies": ["Python", "Django", "PostgreSQL"],
                "url": "https://github.com/user/project"
            }
        ]
    }
    
    response = client.post("/resume", json=resume_data)
    assert response.status_code == 201
    data = response.json()
    assert len(data["data"]["projects"]) == 1
    assert data["data"]["projects"][0]["name"] == "E-commerce Platform"


def test_resume_with_certifications(client):
    """Test creating a resume with certifications"""
    resume_data = {
        "full_name": "Certified Professional",
        "email": "cert@example.com",
        "certifications": [
            {
                "name": "AWS Certified Developer",
                "issuer": "Amazon Web Services",
                "date_obtained": "2023-06-15"
            }
        ]
    }
    
    response = client.post("/resume", json=resume_data)
    assert response.status_code == 201
    data = response.json()
    assert len(data["data"]["certifications"]) == 1
    assert data["data"]["certifications"][0]["name"] == "AWS Certified Developer"
