# Aid Curriculum Backend

Backend API for the Aid Curriculum application built with FastAPI.

## Project Structure

```
aid_curriculum_backend/
├── app/
│   ├── __init__.py          # Application initialization
│   ├── main.py              # FastAPI application factory
│   ├── api/                 # API routes and endpoints
│   │   ├── __init__.py
│   │   ├── router.py        # Main API router
│   │   └── health.py        # Health check endpoint
│   ├── config/              # Configuration files
│   │   ├── __init__.py
│   │   └── settings.py      # Application settings
│   ├── database/            # Database configuration
│   │   ├── __init__.py
│   │   └── connection.py    # Database connection and session
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   └── base.py          # Base model with common fields
│   ├── services/            # Business logic
│   │   └── __init__.py
│   └── utils/               # Utility functions
│       └── __init__.py
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── conftest.py          # Test configuration
│   └── test_health.py       # Health check tests
├── main.py                  # Application entry point
├── setup.py                 # Package setup
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── .env.example             # Example environment variables
├── .gitignore              # Git ignore rules
├── LICENSE                  # License file
└── README.md               # This file
```

## Setup

### Prerequisites

- Python 3.9 or higher
- PostgreSQL (or other supported database)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/LugiaKB/aid_curriculum_backend.git
cd aid_curriculum_backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run database migrations (once implemented):
```bash
alembic upgrade head
```

## Running the Application

### Using Python directly:
```bash
python main.py
```

### Using Uvicorn:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

### Running Tests

```bash
pytest
```

With coverage:
```bash
pytest --cov=app --cov-report=html
```

### Code Formatting

```bash
black .
```

### Linting

```bash
ruff check .
```

### Type Checking

```bash
mypy app/
```

## Project Components

### API Layer (`app/api/`)
Define REST API endpoints and routes here. Each module should represent a resource or feature.

### Models Layer (`app/models/`)
Define SQLAlchemy database models here. All models should inherit from `BaseModel`.

### Services Layer (`app/services/`)
Implement business logic and application services here. Services coordinate between API and data layers.

### Database Layer (`app/database/`)
Configure database connections and sessions. Use `get_db()` dependency for database access in routes.

### Configuration (`app/config/`)
Application settings and configuration management using Pydantic Settings.

### Utilities (`app/utils/`)
Reusable utility functions and helper modules.

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## License

See LICENSE file for details.
