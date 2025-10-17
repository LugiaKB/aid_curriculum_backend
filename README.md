# AI Resume Builder Backend

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-00C7B7?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-412991?style=flat&logo=openai)](https://openai.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A FastAPI-based backend with AI integration for intelligent resume building and analysis.

## Features

- 🚀 **FastAPI Framework**: High-performance, modern Python web framework
- 🤖 **AI Integration**: OpenAI GPT integration for intelligent resume generation and analysis
- 📝 **Resume Management**: Full CRUD operations for resumes
- 🎯 **AI Resume Generation**: Generate tailored resume content based on job descriptions
- 📊 **Resume Analysis**: Get AI-powered feedback and scoring on your resume
- 🔍 **Keyword Matching**: Analyze how well your resume matches job requirements
- 📚 **API Documentation**: Auto-generated interactive API docs with Swagger UI

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **OpenAI**: AI-powered content generation and analysis
- **Uvicorn**: Lightning-fast ASGI server

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/LugiaKB/aid_curriculum_backend.git
cd aid_curriculum_backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key (optional, falls back to template-based generation)
```

### Running the Server

Start the development server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint

### Resume Management
- `POST /api/resumes/` - Create a new resume
- `GET /api/resumes/` - List all resumes
- `GET /api/resumes/{resume_id}` - Get a specific resume
- `PUT /api/resumes/{resume_id}` - Update a resume
- `DELETE /api/resumes/{resume_id}` - Delete a resume

### AI-Powered Features
- `POST /api/resumes/generate` - Generate resume content using AI
- `POST /api/resumes/analyze` - Analyze resume and get feedback

## Usage Examples

### Generate Resume Content

```bash
curl -X POST "http://localhost:8000/api/resumes/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Looking for a Python developer with FastAPI experience...",
    "experience_level": "mid-level",
    "include_sections": ["summary", "skills", "experience"]
  }'
```

### Analyze Resume

```bash
curl -X POST "http://localhost:8000/api/resumes/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_content": "Your resume content here...",
    "job_description": "Target job description (optional)..."
  }'
```

### Create Resume

```bash
curl -X POST "http://localhost:8000/api/resumes/" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "professional_title": "Software Engineer",
    "contact": {
      "email": "john.doe@example.com",
      "phone": "+1234567890",
      "location": "New York, NY"
    },
    "education": [],
    "experience": [],
    "projects": [],
    "skills": []
  }'
```

## Project Structure

```
aid_curriculum_backend/
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuration settings
│   ├── models/                # Data models
│   │   ├── __init__.py
│   │   └── resume.py          # Resume model
│   ├── routes/                # API routes
│   │   ├── __init__.py
│   │   └── resumes.py         # Resume endpoints
│   ├── schemas/               # Pydantic schemas
│   │   ├── __init__.py
│   │   └── resume.py          # Resume schemas
│   └── services/              # Business logic
│       ├── __init__.py
│       └── ai_service.py      # AI service
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## Configuration

The application can be configured using environment variables in `.env`:

- `OPENAI_API_KEY`: Your OpenAI API key (optional)
- `API_HOST`: API host (default: 0.0.0.0)
- `API_PORT`: API port (default: 8000)
- `DEBUG`: Enable debug mode (default: True)

## AI Features

### Resume Generation

The AI resume generation feature analyzes job descriptions and generates tailored content including:
- Professional summaries
- Relevant skills lists
- Experience suggestions
- Project ideas

If no OpenAI API key is provided, the system falls back to template-based generation.

### Resume Analysis

The AI analysis feature provides:
- Overall resume score (0-100)
- Strengths identification
- Areas for improvement
- Keyword matching against job descriptions
- Actionable suggestions

## Development

### Adding New Features

1. Create new schemas in `app/schemas/`
2. Add models in `app/models/`
3. Implement business logic in `app/services/`
4. Create routes in `app/routes/`
5. Register routes in `main.py`

### Testing

The API provides interactive testing through Swagger UI at `/docs`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Quick Reference

### Start the Server
```bash
python main.py
# or
./run_server.sh
# or with Docker
docker-compose up
```

### Access the API
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

### Common Operations
```bash
# Generate resume content
curl -X POST http://localhost:8000/api/resumes/generate \
  -H "Content-Type: application/json" \
  -d '{"job_description": "Python developer", "experience_level": "mid-level"}'

# Analyze resume
curl -X POST http://localhost:8000/api/resumes/analyze \
  -H "Content-Type: application/json" \
  -d '{"resume_content": "Your resume text..."}'

# Create resume
curl -X POST http://localhost:8000/api/resumes/ \
  -H "Content-Type: application/json" \
  -d '{"full_name": "John Doe", "contact": {"email": "john@example.com"}}'
```

## Documentation

- 📚 **[Quick Start Guide](QUICKSTART.md)** - Get up and running in 5 minutes
- 📖 **[API Documentation](API_DOCS.md)** - Complete API reference with examples
- 🏗️ **[Architecture Overview](ARCHITECTURE.md)** - System design and architecture
- 🚀 **[Deployment Guide](DEPLOYMENT.md)** - Production deployment instructions
- 🔧 **[Troubleshooting Guide](TROUBLESHOOTING.md)** - Common issues and solutions
- 🤝 **[Contributing Guidelines](CONTRIBUTING.md)** - How to contribute
- 📋 **[Project Summary](PROJECT_SUMMARY.md)** - Complete feature overview

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a Pull Request.