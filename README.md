# Aid Curriculum Backend

AI-powered resume building backend service for Aid Curriculum platform.

## Features

- **AI-Powered Resume Generation**: Uses OpenAI's GPT models to generate professional, ATS-friendly resumes
- **Structured Data Input**: Accepts structured JSON data for personal info, education, experience, and skills
- **Customizable Output**: Supports different tones (professional, creative, technical) and styles (modern, classic, minimal)
- **Fallback Support**: Works without AI by generating basic formatted resumes
- **RESTful API**: Built with FastAPI for high performance and easy integration
- **Smart Suggestions**: Provides AI-generated suggestions for resume improvement

## Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (optional, but recommended for AI features)

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

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

4. Run the server:
```bash
python -m app.main
# Or use uvicorn directly:
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

#### POST `/api/resume/generate`

Generate a professional resume from structured data.

**Request Body:**
```json
{
  "resume_data": {
    "personal_info": {
      "full_name": "John Doe",
      "email": "john.doe@example.com",
      "phone": "+1-234-567-8900",
      "location": "San Francisco, CA",
      "linkedin": "https://linkedin.com/in/johndoe",
      "github": "https://github.com/johndoe",
      "summary": "Experienced software engineer with 5+ years in full-stack development"
    },
    "education": [
      {
        "institution": "Stanford University",
        "degree": "Bachelor of Science",
        "field_of_study": "Computer Science",
        "start_date": "2015-09",
        "end_date": "2019-06",
        "gpa": "3.8/4.0"
      }
    ],
    "experience": [
      {
        "company": "Tech Corp",
        "position": "Senior Software Engineer",
        "location": "San Francisco, CA",
        "start_date": "2020-01",
        "end_date": "Present",
        "responsibilities": [
          "Led development of microservices architecture serving 1M+ users",
          "Improved system performance by 40% through optimization",
          "Mentored team of 5 junior engineers"
        ]
      }
    ],
    "skills": [
      {
        "category": "Programming Languages",
        "items": ["Python", "JavaScript", "TypeScript", "Go"]
      },
      {
        "category": "Frameworks",
        "items": ["FastAPI", "React", "Node.js", "Django"]
      }
    ],
    "certifications": [
      "AWS Certified Solutions Architect",
      "Google Cloud Professional"
    ],
    "languages": ["English (Native)", "Spanish (Intermediate)"]
  },
  "target_role": "Senior Full Stack Engineer",
  "tone": "professional",
  "format_style": "modern"
}
```

**Response:**
```json
{
  "markdown_content": "# John Doe\n\njohn.doe@example.com | +1-234-567-8900...",
  "html_content": null,
  "suggestions": [
    "Your resume looks comprehensive! Consider tailoring it for specific job applications"
  ]
}
```

## Configuration

Environment variables can be set in `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | None |
| `OPENAI_MODEL` | OpenAI model to use | gpt-4 |
| `OPENAI_TEMPERATURE` | Temperature for AI generation | 0.7 |
| `OPENAI_MAX_TOKENS` | Maximum tokens in response | 2000 |
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8000 |
| `DEBUG` | Enable debug mode | false |

## Project Structure

```
aid_curriculum_backend/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application and routes
│   ├── models.py            # Pydantic models for data validation
│   ├── services.py          # AI resume generation service
│   └── config.py            # Configuration management
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Style

The project follows PEP 8 style guidelines. Use tools like `black` and `flake8`:

```bash
pip install black flake8
black app/
flake8 app/
```

## API Usage Examples

### Using cURL

```bash
curl -X POST "http://localhost:8000/api/resume/generate" \
  -H "Content-Type: application/json" \
  -d @sample_resume_data.json
```

### Using Python

```python
import requests

resume_data = {
    "resume_data": {
        "personal_info": {
            "full_name": "Jane Smith",
            "email": "jane@example.com",
            # ... more fields
        },
        # ... more sections
    },
    "target_role": "Data Scientist",
    "tone": "professional"
}

response = requests.post(
    "http://localhost:8000/api/resume/generate",
    json=resume_data
)

resume = response.json()
print(resume["markdown_content"])
```

## Features in Detail

### AI Resume Generation

The service uses OpenAI's language models to:
- Rewrite and enhance descriptions with action verbs
- Optimize content for ATS (Applicant Tracking Systems)
- Tailor content based on target role
- Maintain consistent tone and style
- Highlight quantifiable achievements

### Fallback Mode

When OpenAI API key is not configured or API is unavailable:
- Generates clean, formatted resumes using templates
- Maintains all structural elements
- Still provides basic improvement suggestions
- Ensures service availability

### Customization Options

**Tone Options:**
- `professional`: Formal and achievement-focused
- `creative`: Engaging and personality-driven
- `technical`: Precise and methodology-focused

**Style Options:**
- `modern`: Clean with clear sections and bullet points
- `classic`: Traditional with formal language
- `minimal`: Concise with key information only

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or contributions, please open an issue in the GitHub repository.