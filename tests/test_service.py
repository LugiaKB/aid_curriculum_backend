"""
Unit tests for GeminiService

These tests verify the service layer functionality.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.gemini.service import GeminiService


class TestGeminiService:
    """Test cases for GeminiService"""
    
    @patch('src.gemini.service.GeminiClient')
    def test_init(self, mock_client_class):
        """Test service initialization"""
        service = GeminiService(api_key="test_key", model_name="gemini-pro")
        mock_client_class.assert_called_once_with(
            api_key="test_key",
            model_name="gemini-pro"
        )
    
    @patch('src.gemini.service.GeminiClient')
    def test_generate_curriculum_content(self, mock_client_class):
        """Test curriculum content generation"""
        mock_client = MagicMock()
        mock_client.generate_content.return_value = "Generated curriculum"
        mock_client_class.return_value = mock_client
        
        service = GeminiService(api_key="test_key")
        result = service.generate_curriculum_content(
            topic="Photosynthesis",
            grade_level="8th grade",
            subject="Biology"
        )
        
        assert result == "Generated curriculum"
        # Verify that generate_content was called with a prompt containing the topic
        call_args = mock_client.generate_content.call_args
        assert "Photosynthesis" in call_args[0][0]
        assert "8th grade" in call_args[0][0]
        assert "Biology" in call_args[0][0]
    
    @patch('src.gemini.service.GeminiClient')
    def test_explain_concept(self, mock_client_class):
        """Test concept explanation"""
        mock_client = MagicMock()
        mock_client.generate_content.return_value = "Concept explanation"
        mock_client_class.return_value = mock_client
        
        service = GeminiService(api_key="test_key")
        result = service.explain_concept(
            concept="Pythagorean theorem",
            complexity_level="simple"
        )
        
        assert result == "Concept explanation"
        call_args = mock_client.generate_content.call_args
        assert "Pythagorean theorem" in call_args[0][0]
        assert "simple" in call_args[0][0]
    
    @patch('src.gemini.service.GeminiClient')
    def test_generate_quiz_questions(self, mock_client_class):
        """Test quiz question generation"""
        mock_client = MagicMock()
        mock_client.generate_content.return_value = "Quiz questions"
        mock_client_class.return_value = mock_client
        
        service = GeminiService(api_key="test_key")
        result = service.generate_quiz_questions(
            topic="World War II",
            num_questions=5,
            question_type="multiple choice"
        )
        
        assert result == "Quiz questions"
        call_args = mock_client.generate_content.call_args
        assert "World War II" in call_args[0][0]
        assert "5" in call_args[0][0]
        assert "multiple choice" in call_args[0][0]
    
    @patch('src.gemini.service.GeminiClient')
    def test_create_lesson_plan(self, mock_client_class):
        """Test lesson plan creation"""
        mock_client = MagicMock()
        mock_client.generate_content.return_value = "Lesson plan"
        mock_client_class.return_value = mock_client
        
        service = GeminiService(api_key="test_key")
        result = service.create_lesson_plan(
            topic="Algebra",
            duration="60 minutes",
            grade_level="7th grade",
            learning_objectives=["Understand variables", "Solve equations"]
        )
        
        assert result == "Lesson plan"
        call_args = mock_client.generate_content.call_args
        prompt = call_args[0][0]
        assert "Algebra" in prompt
        assert "60 minutes" in prompt
        assert "7th grade" in prompt
        assert "Understand variables" in prompt
        assert "Solve equations" in prompt
    
    @patch('src.gemini.service.GeminiClient')
    def test_provide_feedback(self, mock_client_class):
        """Test feedback generation"""
        mock_client = MagicMock()
        mock_client.generate_content.return_value = "Feedback"
        mock_client_class.return_value = mock_client
        
        service = GeminiService(api_key="test_key")
        result = service.provide_feedback(
            student_work="Essay content",
            rubric="Grammar, clarity, structure"
        )
        
        assert result == "Feedback"
        call_args = mock_client.generate_content.call_args
        prompt = call_args[0][0]
        assert "Essay content" in prompt
        assert "Grammar, clarity, structure" in prompt
    
    @patch('src.gemini.service.GeminiClient')
    def test_start_tutoring_session(self, mock_client_class):
        """Test tutoring session start"""
        mock_chat_session = MagicMock()
        mock_client = MagicMock()
        mock_client.chat.return_value = mock_chat_session
        mock_client_class.return_value = mock_client
        
        service = GeminiService(api_key="test_key")
        result = service.start_tutoring_session(
            subject="Mathematics",
            initial_question="Help with fractions"
        )
        
        assert result == mock_chat_session
        mock_client.chat.assert_called_once()
    
    @patch('src.gemini.service.GeminiClient')
    def test_summarize_content(self, mock_client_class):
        """Test content summarization"""
        mock_client = MagicMock()
        mock_client.generate_content.return_value = "Summary"
        mock_client_class.return_value = mock_client
        
        service = GeminiService(api_key="test_key")
        result = service.summarize_content(
            content="Long content here",
            length="brief"
        )
        
        assert result == "Summary"
        call_args = mock_client.generate_content.call_args
        prompt = call_args[0][0]
        assert "Long content here" in prompt
        assert "brief" in prompt
