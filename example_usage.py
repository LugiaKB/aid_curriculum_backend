"""
Example usage of the AI Resume Builder API.

This script demonstrates how to interact with the API endpoints.
Note: The server must be running at http://localhost:8000
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def print_response(title, response):
    """Helper function to print API responses."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")


def test_health_check():
    """Test the health check endpoint."""
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    return response


def test_generate_resume():
    """Test AI resume generation."""
    payload = {
        "job_description": "We are looking for a Python Backend Developer with FastAPI experience. "
                          "The ideal candidate should have strong knowledge of REST APIs, "
                          "database design, and cloud deployment. Experience with AI/ML is a plus.",
        "experience_level": "mid-level",
        "include_sections": ["summary", "skills", "experience", "projects"]
    }
    
    response = requests.post(
        f"{BASE_URL}/api/resumes/generate",
        json=payload
    )
    print_response("Generate Resume Content", response)
    return response


def test_analyze_resume():
    """Test resume analysis."""
    payload = {
        "resume_content": """
        John Doe
        Software Engineer
        
        Professional Summary:
        Experienced software engineer with 5 years of experience in Python development.
        Strong background in building scalable web applications and RESTful APIs.
        
        Skills:
        - Python, FastAPI, Django
        - PostgreSQL, MongoDB
        - Docker, Kubernetes
        - AWS, GCP
        
        Experience:
        Senior Software Engineer at Tech Company (2020-Present)
        - Developed and maintained microservices architecture
        - Implemented CI/CD pipelines
        - Mentored junior developers
        """,
        "job_description": "Looking for a Python developer with FastAPI and cloud experience"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/resumes/analyze",
        json=payload
    )
    print_response("Analyze Resume", response)
    return response


def test_create_resume():
    """Test creating a resume."""
    payload = {
        "full_name": "Jane Smith",
        "professional_title": "Full Stack Developer",
        "summary": "Passionate developer with expertise in modern web technologies",
        "contact": {
            "email": "jane.smith@example.com",
            "phone": "+1-555-0123",
            "location": "San Francisco, CA",
            "linkedin": "linkedin.com/in/janesmith",
            "github": "github.com/janesmith"
        },
        "education": [
            {
                "institution": "University of California",
                "degree": "Bachelor of Science",
                "field_of_study": "Computer Science",
                "start_date": "2015",
                "end_date": "2019",
                "gpa": "3.8"
            }
        ],
        "experience": [
            {
                "company": "Tech Startup Inc",
                "position": "Full Stack Developer",
                "location": "San Francisco, CA",
                "start_date": "2019-06",
                "end_date": "2023-12",
                "current": False,
                "description": "Developed web applications using React and Node.js",
                "achievements": [
                    "Improved application performance by 40%",
                    "Led migration to microservices architecture"
                ]
            }
        ],
        "projects": [
            {
                "name": "E-commerce Platform",
                "description": "Built a scalable e-commerce platform",
                "technologies": ["React", "Node.js", "MongoDB"],
                "url": "https://github.com/janesmith/ecommerce"
            }
        ],
        "skills": [
            {
                "category": "Frontend",
                "skills": ["React", "Vue.js", "TypeScript"]
            },
            {
                "category": "Backend",
                "skills": ["Node.js", "Python", "FastAPI"]
            }
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/api/resumes/",
        json=payload
    )
    print_response("Create Resume", response)
    return response


def test_list_resumes():
    """Test listing all resumes."""
    response = requests.get(f"{BASE_URL}/api/resumes/")
    print_response("List Resumes", response)
    return response


def main():
    """Run all example tests."""
    print("\n" + "="*60)
    print("AI Resume Builder API - Example Usage")
    print("="*60)
    print("\nMake sure the server is running at http://localhost:8000")
    print("Start the server with: python main.py")
    print("\nPress Enter to continue or Ctrl+C to exit...")
    input()
    
    try:
        # Test health check
        test_health_check()
        
        # Test AI features
        test_generate_resume()
        test_analyze_resume()
        
        # Test CRUD operations
        test_create_resume()
        test_list_resumes()
        
        print("\n" + "="*60)
        print("All tests completed!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the server.")
        print("Make sure the server is running at http://localhost:8000")
        print("Start it with: python main.py")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
