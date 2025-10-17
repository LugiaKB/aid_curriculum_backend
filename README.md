# Aid Curriculum Backend

A backend service for educational curriculum management with Google Gemini AI integration.

## Features

- **Gemini AI Integration**: Leverage Google's Gemini API for educational content generation
- **Curriculum Content Generation**: Create educational content for various topics and grade levels
- **Lesson Planning**: Generate comprehensive lesson plans with objectives and activities
- **Quiz Generation**: Automatically create quiz questions for assessment
- **Interactive Tutoring**: Start chat-based tutoring sessions
- **Content Summarization**: Summarize educational materials
- **Feedback Generation**: Provide constructive feedback on student work

## Installation

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
# Edit .env and add your Gemini API key
```

## Configuration

Create a `.env` file with the following variables:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-pro
```

Get your Gemini API key from: https://makersuite.google.com/app/apikey

## Usage

### Basic Client Usage

```python
from src.gemini.client import GeminiClient

# Initialize the client
client = GeminiClient()

# Generate content
response = client.generate_content("Explain photosynthesis")
print(response)

# Stream content
for chunk in client.generate_content_stream("Write a story about space"):
    print(chunk, end="")

# Start a chat session
chat = client.chat()
response = chat.send_message("What is the capital of France?")
print(response)
```

### Service Layer Usage

```python
from src.gemini.service import GeminiService

# Initialize the service
service = GeminiService()

# Generate curriculum content
content = service.generate_curriculum_content(
    topic="Photosynthesis",
    grade_level="8th grade",
    subject="Biology"
)
print(content)

# Explain a concept
explanation = service.explain_concept(
    concept="Pythagorean theorem",
    complexity_level="simple"
)
print(explanation)

# Generate quiz questions
quiz = service.generate_quiz_questions(
    topic="World War II",
    num_questions=5,
    question_type="multiple choice"
)
print(quiz)

# Create a lesson plan
lesson = service.create_lesson_plan(
    topic="Introduction to Algebra",
    duration="60 minutes",
    grade_level="7th grade",
    learning_objectives=[
        "Understand variables and constants",
        "Solve simple linear equations"
    ]
)
print(lesson)

# Start tutoring session
chat = service.start_tutoring_session(
    subject="Mathematics",
    initial_question="Can you help me with fractions?"
)
response = chat.send_message("How do I add 1/2 and 1/3?")
print(response)

# Provide feedback on student work
feedback = service.provide_feedback(
    student_work="The mitochondria is the powerhouse of the cell...",
    rubric="Accuracy, clarity, depth of explanation"
)
print(feedback)

# Summarize content
summary = service.summarize_content(
    content="Long educational text here...",
    length="brief"
)
print(summary)
```

## Project Structure

```
aid_curriculum_backend/
├── src/
│   ├── __init__.py
│   └── gemini/
│       ├── __init__.py
│       ├── client.py      # Low-level Gemini API client
│       └── service.py     # High-level business logic service
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## API Reference

### GeminiClient

Low-level client for direct API interaction:

- `generate_content(prompt, **kwargs)`: Generate content from a prompt
- `generate_content_stream(prompt, **kwargs)`: Generate content with streaming
- `chat(history)`: Start a chat session

### GeminiService

High-level service with educational use cases:

- `generate_curriculum_content(topic, grade_level, subject, **kwargs)`: Generate curriculum content
- `explain_concept(concept, complexity_level, **kwargs)`: Explain educational concepts
- `generate_quiz_questions(topic, num_questions, question_type, **kwargs)`: Create quiz questions
- `create_lesson_plan(topic, duration, grade_level, learning_objectives, **kwargs)`: Generate lesson plans
- `provide_feedback(student_work, rubric, **kwargs)`: Generate feedback on student work
- `start_tutoring_session(subject, initial_question)`: Start interactive tutoring
- `summarize_content(content, length, **kwargs)`: Summarize educational content

## License

See [LICENSE](LICENSE) file for details.