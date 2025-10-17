# API Documentation

## Overview

The AI Resume Builder API provides endpoints for creating, managing, and enhancing resumes with AI-powered features.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. This should be added for production use.

## Endpoints

### Health Check

#### GET /health
Check if the API is running.

**Response**
```json
{
  "status": "healthy",
  "api_version": "1.0.0"
}
```

---

### Resume Management

#### POST /api/resumes/
Create a new resume.

**Request Body**
```json
{
  "full_name": "John Doe",
  "professional_title": "Software Engineer",
  "summary": "Experienced software engineer...",
  "contact": {
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "location": "New York, NY",
    "linkedin": "linkedin.com/in/johndoe",
    "github": "github.com/johndoe"
  },
  "education": [
    {
      "institution": "University Name",
      "degree": "Bachelor of Science",
      "field_of_study": "Computer Science",
      "start_date": "2015",
      "end_date": "2019",
      "gpa": "3.8"
    }
  ],
  "experience": [
    {
      "company": "Company Name",
      "position": "Software Engineer",
      "location": "City, State",
      "start_date": "2019-06",
      "end_date": "2023-12",
      "current": false,
      "description": "Job responsibilities...",
      "achievements": [
        "Achievement 1",
        "Achievement 2"
      ]
    }
  ],
  "projects": [
    {
      "name": "Project Name",
      "description": "Project description",
      "technologies": ["Python", "FastAPI"],
      "url": "https://github.com/user/project"
    }
  ],
  "skills": [
    {
      "category": "Programming Languages",
      "skills": ["Python", "JavaScript", "Java"]
    }
  ]
}
```

**Response** (201 Created)
```json
{
  "id": "uuid-here",
  "full_name": "John Doe",
  ...
}
```

#### GET /api/resumes/
List all resumes.

**Response** (200 OK)
```json
[
  {
    "id": "uuid-1",
    "full_name": "John Doe",
    ...
  },
  {
    "id": "uuid-2",
    "full_name": "Jane Smith",
    ...
  }
]
```

#### GET /api/resumes/{resume_id}
Get a specific resume by ID.

**Response** (200 OK)
```json
{
  "id": "uuid-here",
  "full_name": "John Doe",
  ...
}
```

**Error Response** (404 Not Found)
```json
{
  "detail": "Resume with id {resume_id} not found"
}
```

#### PUT /api/resumes/{resume_id}
Update an existing resume.

**Request Body**: Same as POST /api/resumes/

**Response** (200 OK): Updated resume object

#### DELETE /api/resumes/{resume_id}
Delete a resume.

**Response** (204 No Content)

---

### AI Features

#### POST /api/resumes/generate
Generate resume content using AI based on a job description.

**Request Body**
```json
{
  "job_description": "We are looking for a Python developer with FastAPI experience...",
  "user_info": "Optional: Your background information or existing resume content",
  "experience_level": "mid-level",
  "include_sections": ["summary", "skills", "experience", "projects"]
}
```

**Parameters**
- `job_description` (required): The job posting or description
- `user_info` (optional): Additional context about the user
- `experience_level` (optional): One of: "entry-level", "mid-level", "senior", "expert"
- `include_sections` (optional): Array of sections to generate

**Response** (200 OK)
```json
{
  "generated_content": {
    "professional_summary": "Motivated mid-level professional...",
    "skills": ["Python", "FastAPI", "REST APIs", "Docker"],
    "experience_suggestions": [
      "Highlight quantifiable achievements",
      "Use action verbs"
    ],
    "project_ideas": [
      "Describe technical projects that demonstrate relevant skills"
    ]
  },
  "suggestions": [
    "Review and customize the generated content",
    "Add specific metrics and achievements"
  ]
}
```

#### POST /api/resumes/analyze
Analyze a resume and provide feedback.

**Request Body**
```json
{
  "resume_content": "Your complete resume text here...",
  "job_description": "Optional: Target job description for keyword matching"
}
```

**Parameters**
- `resume_content` (required): The resume text to analyze
- `job_description` (optional): Job description for targeted analysis

**Response** (200 OK)
```json
{
  "score": 75.0,
  "strengths": [
    "Well-formatted content",
    "Clear professional summary"
  ],
  "improvements": [
    "Add more quantifiable achievements",
    "Include relevant keywords"
  ],
  "keywords_match": {
    "matched": ["Python", "API", "Docker"],
    "missing": ["Kubernetes", "CI/CD"]
  },
  "suggestions": [
    "Tailor your resume to each job application",
    "Use action verbs to describe responsibilities"
  ]
}
```

---

## Data Models

### ContactInfo
```json
{
  "email": "required@example.com",
  "phone": "optional",
  "location": "optional",
  "linkedin": "optional",
  "github": "optional",
  "website": "optional"
}
```

### Education
```json
{
  "institution": "required",
  "degree": "required",
  "field_of_study": "optional",
  "start_date": "optional",
  "end_date": "optional",
  "gpa": "optional",
  "description": "optional"
}
```

### Experience
```json
{
  "company": "required",
  "position": "required",
  "location": "optional",
  "start_date": "optional",
  "end_date": "optional",
  "current": false,
  "description": "optional",
  "achievements": []
}
```

### Project
```json
{
  "name": "required",
  "description": "required",
  "technologies": [],
  "url": "optional",
  "start_date": "optional",
  "end_date": "optional"
}
```

### Skill
```json
{
  "category": "required",
  "skills": ["required array"]
}
```

---

## Error Responses

All endpoints may return the following error responses:

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error message"
}
```

---

## Interactive Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive API documentation where you can test all endpoints.

---

## AI Configuration

The AI features require an OpenAI API key. Set it in your `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

If no API key is provided, the system will fall back to template-based generation, which still provides useful resume suggestions but without AI-powered customization.
