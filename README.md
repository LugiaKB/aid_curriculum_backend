# CV Generator API

A simple FastAPI application that generates professional CVs using Google's Gemini AI.

## Setup

1. Install pipenv if you haven't already:
```bash
pip install pipenv
```

2. Install dependencies:
```bash
pipenv install
```

3. Copy `.env.example` to `.env` and add your Google API key:
```bash
GOOGLE_API_KEY=your_api_key_here
```

4. Run the application:

To start the API server:
```bash
pipenv run api
```
The API will be available at `http://localhost:8000`

To test CV generation locally with example data:
```bash
pipenv run generate
```

## API Usage

Send a POST request to `/generate-cv` with the following JSON structure:

```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "summary": "Experienced software developer...",
    "education": [
        "BS in Computer Science, University XYZ, 2018-2022"
    ],
    "experience": [
        "Software Developer at Company ABC, 2022-Present"
    ],
    "skills": [
        "Python",
        "FastAPI",
        "Machine Learning"
    ]
}
```

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation at: `http://localhost:8000/docs`
- ReDoc documentation at: `http://localhost:8000/redoc`