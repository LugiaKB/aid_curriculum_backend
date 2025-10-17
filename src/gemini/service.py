"""
Gemini Service

This module provides a high-level service layer for Gemini AI operations,
implementing business logic and use cases for the aid curriculum backend.
"""

from typing import Optional, Dict, Any, List
from .client import GeminiClient, ChatSession


class GeminiService:
    """
    Service layer for Gemini AI operations.
    
    This service provides high-level methods for common use cases
    in the aid curriculum backend, such as content generation,
    curriculum assistance, and educational content creation.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gemini-pro"
    ):
        """
        Initialize the Gemini service.
        
        Args:
            api_key: Gemini API key. If not provided, will use environment variable.
            model_name: Name of the Gemini model to use.
        """
        self.client = GeminiClient(api_key=api_key, model_name=model_name)
    
    def generate_curriculum_content(
        self,
        topic: str,
        grade_level: Optional[str] = None,
        subject: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        """
        Generate educational curriculum content.
        
        Args:
            topic: The topic to generate content for.
            grade_level: Target grade level (e.g., "5th grade", "high school").
            subject: Subject area (e.g., "math", "science", "history").
            **kwargs: Additional parameters for content generation.
        
        Returns:
            Generated curriculum content.
        """
        prompt_parts = [f"Generate educational content about: {topic}"]
        
        if grade_level:
            prompt_parts.append(f"Target grade level: {grade_level}")
        
        if subject:
            prompt_parts.append(f"Subject: {subject}")
        
        prompt = "\n".join(prompt_parts)
        
        return self.client.generate_content(prompt, **kwargs)
    
    def explain_concept(
        self,
        concept: str,
        complexity_level: str = "intermediate",
        **kwargs: Any
    ) -> str:
        """
        Explain an educational concept.
        
        Args:
            concept: The concept to explain.
            complexity_level: Level of explanation complexity 
                             (e.g., "simple", "intermediate", "advanced").
            **kwargs: Additional parameters for content generation.
        
        Returns:
            Explanation of the concept.
        """
        prompt = (
            f"Explain the following concept at a {complexity_level} level:\n\n"
            f"{concept}\n\n"
            f"Provide a clear and educational explanation."
        )
        
        return self.client.generate_content(prompt, **kwargs)
    
    def generate_quiz_questions(
        self,
        topic: str,
        num_questions: int = 5,
        question_type: str = "multiple choice",
        **kwargs: Any
    ) -> str:
        """
        Generate quiz questions on a given topic.
        
        Args:
            topic: The topic for the quiz questions.
            num_questions: Number of questions to generate.
            question_type: Type of questions (e.g., "multiple choice", "true/false", "short answer").
            **kwargs: Additional parameters for content generation.
        
        Returns:
            Generated quiz questions.
        """
        prompt = (
            f"Generate {num_questions} {question_type} questions about: {topic}\n\n"
            f"Format each question clearly with answer options where applicable."
        )
        
        return self.client.generate_content(prompt, **kwargs)
    
    def create_lesson_plan(
        self,
        topic: str,
        duration: str = "45 minutes",
        grade_level: Optional[str] = None,
        learning_objectives: Optional[List[str]] = None,
        **kwargs: Any
    ) -> str:
        """
        Create a lesson plan for a given topic.
        
        Args:
            topic: The topic for the lesson plan.
            duration: Duration of the lesson.
            grade_level: Target grade level.
            learning_objectives: List of learning objectives.
            **kwargs: Additional parameters for content generation.
        
        Returns:
            Generated lesson plan.
        """
        prompt_parts = [
            f"Create a detailed lesson plan for: {topic}",
            f"Duration: {duration}"
        ]
        
        if grade_level:
            prompt_parts.append(f"Grade level: {grade_level}")
        
        if learning_objectives:
            prompt_parts.append("Learning objectives:")
            for obj in learning_objectives:
                prompt_parts.append(f"- {obj}")
        
        prompt_parts.append(
            "\nInclude: introduction, main activities, assessment, and conclusion."
        )
        
        prompt = "\n".join(prompt_parts)
        
        return self.client.generate_content(prompt, **kwargs)
    
    def provide_feedback(
        self,
        student_work: str,
        rubric: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        """
        Generate feedback on student work.
        
        Args:
            student_work: The student's work to evaluate.
            rubric: Optional rubric to evaluate against.
            **kwargs: Additional parameters for content generation.
        
        Returns:
            Generated feedback.
        """
        prompt_parts = ["Provide constructive feedback on the following student work:\n"]
        prompt_parts.append(student_work)
        
        if rubric:
            prompt_parts.append(f"\n\nEvaluation rubric:\n{rubric}")
        
        prompt_parts.append(
            "\n\nProvide specific, actionable feedback that is encouraging and educational."
        )
        
        prompt = "\n".join(prompt_parts)
        
        return self.client.generate_content(prompt, **kwargs)
    
    def start_tutoring_session(
        self,
        subject: str,
        initial_question: Optional[str] = None
    ) -> ChatSession:
        """
        Start an interactive tutoring chat session.
        
        Args:
            subject: The subject for tutoring.
            initial_question: Optional initial question from the student.
        
        Returns:
            A ChatSession object for interactive tutoring.
        """
        history = []
        
        if initial_question:
            system_prompt = (
                f"You are a helpful tutor for {subject}. "
                f"Provide clear, educational explanations and encourage learning."
            )
            history.append({
                "role": "user",
                "parts": [system_prompt]
            })
            history.append({
                "role": "model",
                "parts": ["I understand. I'm here to help you learn about " + subject + ". What would you like to know?"]
            })
        
        return self.client.chat(history=history)
    
    def summarize_content(
        self,
        content: str,
        length: str = "brief",
        **kwargs: Any
    ) -> str:
        """
        Summarize educational content.
        
        Args:
            content: The content to summarize.
            length: Desired summary length ("brief", "moderate", "detailed").
            **kwargs: Additional parameters for content generation.
        
        Returns:
            Summary of the content.
        """
        prompt = (
            f"Provide a {length} summary of the following content:\n\n"
            f"{content}"
        )
        
        return self.client.generate_content(prompt, **kwargs)
