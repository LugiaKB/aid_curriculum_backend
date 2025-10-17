"""
Example usage of the Gemini integration.

This script demonstrates how to use the GeminiClient and GeminiService.
Make sure to set GEMINI_API_KEY in your .env file before running.
"""

import os
from dotenv import load_dotenv
from src.gemini.client import GeminiClient
from src.gemini.service import GeminiService


def main():
    # Load environment variables
    load_dotenv()
    
    # Check if API key is set
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY not found in environment variables.")
        print("Please set it in your .env file.")
        return
    
    print("=== Gemini Integration Example ===\n")
    
    # Example 1: Basic client usage
    print("1. Basic Client Usage:")
    print("-" * 50)
    client = GeminiClient()
    response = client.generate_content("Explain what photosynthesis is in one sentence.")
    print(f"Response: {response}\n")
    
    # Example 2: Service layer usage
    print("2. Generate Curriculum Content:")
    print("-" * 50)
    service = GeminiService()
    content = service.generate_curriculum_content(
        topic="The Water Cycle",
        grade_level="5th grade",
        subject="Science"
    )
    print(f"Content:\n{content}\n")
    
    # Example 3: Explain a concept
    print("3. Explain a Concept:")
    print("-" * 50)
    explanation = service.explain_concept(
        concept="Pythagorean theorem",
        complexity_level="simple"
    )
    print(f"Explanation:\n{explanation}\n")
    
    # Example 4: Generate quiz questions
    print("4. Generate Quiz Questions:")
    print("-" * 50)
    quiz = service.generate_quiz_questions(
        topic="Solar System",
        num_questions=3,
        question_type="multiple choice"
    )
    print(f"Quiz:\n{quiz}\n")
    
    print("=== Examples completed successfully ===")


if __name__ == "__main__":
    main()
