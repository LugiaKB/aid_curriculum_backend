# AID Curriculum Backend

A FastAPI-based backend service for building and managing resumes. This API provides endpoints to create, retrieve, update, and delete resume data without requiring a database connection (data is stored in-memory).

## Features

- **Create Resume**: Submit resume data with personal information, experience, education, projects, certifications, and more
- **Retrieve Resume**: Get resume data by unique ID
- **Update Resume**: Modify existing resume data
- **Delete Resume**: Remove resume data
- **List Resumes**: View all stored resume IDs
- **Comprehensive Data Models**: Support for experience, education, projects, certifications, skills, and more
- **Data Validation**: Email validation and required field checks using Pydantic
- **CORS Support**: Pre-configured for cross-origin requests

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/LugiaKB/aid_curriculum_backend.git
cd aid_curriculum_backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Development Server

Start the development server with hot-reload:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Production Server

For production, run without the `--reload` flag:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:

- **Interactive API Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Documentation (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### Root Endpoint
- **GET** `/` - Welcome message and available endpoints

### Resume Operations

#### Create Resume
- **POST** `/resume`
- **Body**: Resume data (JSON)
- **Returns**: Created resume with status and message

Example request:
```json
{
  "full_name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "location": "New York, NY",
  "summary": "Experienced software engineer with 5+ years",
  "skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
  "experience": [
    {
      "company": "Tech Corp",
      "position": "Senior Software Engineer",
      "location": "New York, NY",
      "start_date": "2020-01-01",
      "description": "Led development of microservices architecture",
      "is_current": true
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
  ],
  "projects": [
    {
      "name": "E-commerce Platform",
      "description": "Built a scalable e-commerce platform",
      "technologies": ["Python", "Django", "PostgreSQL"],
      "url": "https://github.com/user/project"
    }
  ],
  "certifications": [
    {
      "name": "AWS Certified Developer",
      "issuer": "Amazon Web Services",
      "date_obtained": "2023-06-15"
    }
  ]
}
```

#### Get Resume
- **GET** `/resume/{resume_id}`
- **Returns**: Resume data for the specified ID

#### Update Resume
- **PUT** `/resume/{resume_id}`
- **Body**: Updated resume data (JSON)
- **Returns**: Updated resume data

#### Delete Resume
- **DELETE** `/resume/{resume_id}`
- **Returns**: Success confirmation

#### List All Resumes
- **GET** `/resumes`
- **Returns**: Count and list of all resume IDs

## Data Model

The resume data structure includes:

### Required Fields
- `full_name`: Full name (string)
- `email`: Email address (validated)

### Optional Fields
- `phone`: Phone number
- `location`: City, State/Country
- `linkedin`: LinkedIn profile URL
- `github`: GitHub profile URL
- `website`: Personal website URL
- `summary`: Professional summary or objective
- `skills`: List of skills
- `experience`: List of work experience entries
- `education`: List of education entries
- `projects`: List of project entries
- `certifications`: List of certification entries
- `languages`: List of languages spoken
- `interests`: List of interests and hobbies

### Experience Entry
- `company`: Company name (required)
- `position`: Job title/position (required)
- `location`: Location of job
- `start_date`: Start date (YYYY-MM-DD format)
- `end_date`: End date (null if current)
- `description`: Job responsibilities and achievements
- `is_current`: Whether this is current position (default: false)

### Education Entry
- `institution`: Name of educational institution (required)
- `degree`: Degree or certification obtained (required)
- `field_of_study`: Field of study
- `start_date`: Start date (YYYY-MM-DD format)
- `end_date`: End date or expected graduation
- `gpa`: GPA or grade
- `description`: Additional details

### Project Entry
- `name`: Project name (required)
- `description`: Project description (required)
- `technologies`: List of technologies used
- `url`: Project URL
- `start_date`: Start date (YYYY-MM-DD format)
- `end_date`: End date

### Certification Entry
- `name`: Certification name (required)
- `issuer`: Issuing organization (required)
- `date_obtained`: Date obtained (YYYY-MM-DD format)
- `expiry_date`: Expiry date if applicable
- `credential_id`: Credential ID

## Testing

Run the test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=app tests/
```

Run tests with verbose output:

```bash
pytest -v
```

## Development

### Project Structure

```
aid_curriculum_backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and endpoints
│   └── models.py        # Pydantic data models
├── tests/
│   ├── __init__.py
│   └── test_main.py     # API endpoint tests
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

### Key Technologies

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and settings management using Python type annotations
- **Uvicorn**: Lightning-fast ASGI server
- **Pytest**: Testing framework
- **HTTPX**: HTTP client for testing

## Notes

- This version stores data in-memory, so all data will be lost when the server restarts
- Database integration can be added in future iterations
- The API includes CORS middleware configured to allow all origins (adjust for production use)
- Email validation is performed on the `email` field
- Date fields accept ISO 8601 format (YYYY-MM-DD)

## License

See LICENSE file for details.