# Contributing to AI Resume Builder Backend

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/aid_curriculum_backend.git
   cd aid_curriculum_backend
   ```
3. **Set up the development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

## Development Workflow

1. **Create a new branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines

3. **Test your changes**:
   ```bash
   pytest tests/
   ```

4. **Commit your changes** with clear, descriptive messages:
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** on GitHub

## Code Style Guidelines

### Python Code Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Maximum line length: 100 characters

Example:
```python
def calculate_resume_score(resume_content: str, job_description: str) -> float:
    """
    Calculate a match score between resume and job description.
    
    Args:
        resume_content: The resume text to analyze
        job_description: The target job description
        
    Returns:
        A score between 0 and 100
    """
    # Implementation here
    pass
```

### Code Organization

- Place new models in `app/models/`
- Place new schemas in `app/schemas/`
- Place business logic in `app/services/`
- Place API routes in `app/routes/`
- Keep related functionality together

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for good test coverage
- Use descriptive test names

Example:
```python
def test_generate_resume_returns_valid_content():
    """Test that resume generation returns properly formatted content."""
    # Test implementation
    pass
```

## Types of Contributions

### Bug Reports

When reporting bugs, include:
- Python version
- FastAPI version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages or logs

### Feature Requests

When suggesting features:
- Describe the use case
- Explain the expected behavior
- Consider backward compatibility
- Discuss implementation approach

### Code Contributions

Areas where contributions are welcome:
- **New AI features**: Enhanced resume analysis, content suggestions
- **Database integration**: Replace in-memory storage with actual database
- **Authentication**: Add user authentication and authorization
- **Additional endpoints**: Resume templates, cover letter generation
- **Testing**: Improve test coverage
- **Documentation**: Improve or translate documentation
- **Performance**: Optimization and caching
- **Security**: Security improvements

## Pull Request Process

1. **Update documentation** if needed (README, API_DOCS, etc.)
2. **Add tests** for new functionality
3. **Ensure all tests pass**
4. **Update CHANGELOG** if significant changes
5. **Follow the PR template** (if available)
6. **Be responsive** to review feedback

### PR Title Format

Use clear, descriptive titles:
- `feat: Add resume template system`
- `fix: Resolve AI service timeout issue`
- `docs: Update API documentation`
- `test: Add tests for resume analysis`
- `refactor: Improve error handling`

## Development Tips

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run with coverage
pytest --cov=app tests/

# Run with verbose output
pytest -v
```

### Debugging

```bash
# Run server in debug mode
DEBUG=True python main.py

# Use Python debugger
import pdb; pdb.set_trace()
```

### Code Quality Tools

```bash
# Format code (if using black)
black app/

# Lint code (if using flake8)
flake8 app/

# Type checking (if using mypy)
mypy app/
```

## Project Structure

Understanding the project structure:

```
aid_curriculum_backend/
├── app/
│   ├── config.py           # Configuration management
│   ├── models/             # Data models
│   ├── routes/             # API route handlers
│   ├── schemas/            # Pydantic schemas for validation
│   └── services/           # Business logic and AI services
├── tests/                  # Test files
├── main.py                 # Application entry point
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
└── README.md              # Project documentation
```

## Getting Help

- **Documentation**: Check README.md and API_DOCS.md
- **Issues**: Search existing issues on GitHub
- **Questions**: Open a discussion on GitHub

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

## Recognition

Contributors will be recognized in the project documentation.

Thank you for contributing to AI Resume Builder Backend!
