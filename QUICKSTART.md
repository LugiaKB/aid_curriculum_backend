# Quick Start Guide

Get the AI Resume Builder API running in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- pip package manager

## Quick Installation

### Option 1: Standard Setup (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/LugiaKB/aid_curriculum_backend.git
cd aid_curriculum_backend

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment (optional - works without OpenAI key)
cp .env.example .env
# Edit .env to add your OpenAI API key if you have one

# 4. Run the server
python main.py
```

### Option 2: Using Virtual Environment

```bash
# 1. Clone the repository
git clone https://github.com/LugiaKB/aid_curriculum_backend.git
cd aid_curriculum_backend

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
python main.py
```

### Option 3: Using Docker

```bash
# 1. Clone the repository
git clone https://github.com/LugiaKB/aid_curriculum_backend.git
cd aid_curriculum_backend

# 2. Run with Docker Compose
docker-compose up
```

## Verify Installation

Once the server is running, open your browser and visit:

- **API Root**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

You should see the API documentation interface!

## Try It Out

### Using the Interactive Docs (Easiest)

1. Go to http://localhost:8000/docs
2. Click on any endpoint (e.g., "POST /api/resumes/generate")
3. Click "Try it out"
4. Fill in the request body
5. Click "Execute"

### Using curl

Generate resume content:
```bash
curl -X POST "http://localhost:8000/api/resumes/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Python developer with FastAPI experience",
    "experience_level": "mid-level"
  }'
```

Analyze a resume:
```bash
curl -X POST "http://localhost:8000/api/resumes/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_content": "Your resume text here..."
  }'
```

### Using the Example Script

Run the included example script:
```bash
python example_usage.py
```

## What's Next?

- 📚 Read the [full README](README.md) for detailed information
- 📖 Check [API_DOCS.md](API_DOCS.md) for complete API reference
- 🚀 See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- 🤝 Read [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### Port 8000 already in use
Edit `.env` and change `API_PORT=8001`, or:
```bash
# Find and kill the process using port 8000
lsof -i :8000
kill -9 <PID>
```

### OpenAI API errors
The system works without an OpenAI API key! It falls back to template-based generation. If you want to use AI features, add your key to `.env`.

## Need Help?

- Check the documentation in `/docs` when the server is running
- Open an issue on GitHub
- Review the example_usage.py script for code examples

Happy coding! 🎉
