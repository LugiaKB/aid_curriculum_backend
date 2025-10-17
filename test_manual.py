"""
Manual test script for the Resume Builder API

Run this script to test the API functionality:
    python test_manual.py
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_generate_resume():
    """Test resume generation"""
    print("Testing /api/resume/generate endpoint...")
    
    # Load sample data
    with open("sample_resume_data.json", "r") as f:
        data = json.load(f)
    
    response = requests.post(f"{BASE_URL}/api/resume/generate", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n=== Generated Resume ===")
        print(result["markdown_content"][:500] + "...")  # Print first 500 chars
        print(f"\n=== Suggestions ===")
        for suggestion in result["suggestions"]:
            print(f"- {suggestion}")
    else:
        print(f"Error: {response.text}")
    print()


def test_minimal_resume():
    """Test with minimal data"""
    print("Testing with minimal data...")
    
    data = {
        "resume_data": {
            "personal_info": {
                "full_name": "Test User",
                "email": "test@example.com"
            }
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/resume/generate", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("Resume generated successfully!")
        print(f"Content length: {len(result['markdown_content'])} characters")
        print(f"Suggestions: {len(result['suggestions'])} items")
    else:
        print(f"Error: {response.text}")
    print()


if __name__ == "__main__":
    print("=== Aid Curriculum Backend - Resume Builder API Tests ===\n")
    
    try:
        test_health()
        test_generate_resume()
        test_minimal_resume()
        print("✓ All manual tests completed!")
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to server. Make sure the server is running:")
        print("    python -m app.main")
    except Exception as e:
        print(f"ERROR: {e}")
