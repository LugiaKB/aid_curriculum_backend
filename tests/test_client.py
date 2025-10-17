"""
Unit tests for GeminiClient

These tests verify the basic functionality of the Gemini client.
Note: These tests require a valid GEMINI_API_KEY to run integration tests.
"""

import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.gemini.client import GeminiClient, ChatSession


class TestGeminiClient:
    """Test cases for GeminiClient"""
    
    def test_init_with_api_key(self):
        """Test initialization with API key parameter"""
        with patch('google.generativeai.configure'):
            with patch('google.generativeai.GenerativeModel'):
                client = GeminiClient(api_key="test_key", model_name="gemini-pro")
                assert client.api_key == "test_key"
                assert client.model_name == "gemini-pro"
    
    def test_init_with_env_var(self):
        """Test initialization with environment variable"""
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'env_key'}):
            with patch('google.generativeai.configure'):
                with patch('google.generativeai.GenerativeModel'):
                    client = GeminiClient()
                    assert client.api_key == "env_key"
    
    def test_init_without_api_key_raises_error(self):
        """Test that initialization without API key raises ValueError"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Gemini API key must be provided"):
                GeminiClient()
    
    def test_generate_content(self):
        """Test content generation"""
        mock_response = Mock()
        mock_response.text = "Generated content"
        
        with patch('google.generativeai.configure'):
            mock_model = MagicMock()
            mock_model.generate_content.return_value = mock_response
            
            with patch('google.generativeai.GenerativeModel', return_value=mock_model):
                client = GeminiClient(api_key="test_key")
                result = client.generate_content("Test prompt")
                
                assert result == "Generated content"
                mock_model.generate_content.assert_called_once_with("Test prompt")
    
    def test_generate_content_with_kwargs(self):
        """Test content generation with additional parameters"""
        mock_response = Mock()
        mock_response.text = "Generated content"
        
        with patch('google.generativeai.configure'):
            mock_model = MagicMock()
            mock_model.generate_content.return_value = mock_response
            
            with patch('google.generativeai.GenerativeModel', return_value=mock_model):
                client = GeminiClient(api_key="test_key")
                result = client.generate_content("Test prompt", temperature=0.5)
                
                assert result == "Generated content"
                mock_model.generate_content.assert_called_once_with(
                    "Test prompt",
                    temperature=0.5
                )
    
    def test_generate_content_stream(self):
        """Test streaming content generation"""
        mock_chunk1 = Mock()
        mock_chunk1.text = "Part 1 "
        mock_chunk2 = Mock()
        mock_chunk2.text = "Part 2"
        
        with patch('google.generativeai.configure'):
            mock_model = MagicMock()
            mock_model.generate_content.return_value = [mock_chunk1, mock_chunk2]
            
            with patch('google.generativeai.GenerativeModel', return_value=mock_model):
                client = GeminiClient(api_key="test_key")
                chunks = list(client.generate_content_stream("Test prompt"))
                
                assert chunks == ["Part 1 ", "Part 2"]
                mock_model.generate_content.assert_called_once_with(
                    "Test prompt",
                    stream=True
                )
    
    def test_chat_session(self):
        """Test chat session creation"""
        with patch('google.generativeai.configure'):
            mock_model = MagicMock()
            mock_chat = MagicMock()
            mock_model.start_chat.return_value = mock_chat
            
            with patch('google.generativeai.GenerativeModel', return_value=mock_model):
                client = GeminiClient(api_key="test_key")
                chat = client.chat()
                
                assert isinstance(chat, ChatSession)
                mock_model.start_chat.assert_called_once_with(history=[])


class TestChatSession:
    """Test cases for ChatSession"""
    
    def test_send_message(self):
        """Test sending a message in chat session"""
        mock_response = Mock()
        mock_response.text = "Response message"
        
        mock_chat = MagicMock()
        mock_chat.send_message.return_value = mock_response
        
        session = ChatSession(mock_chat)
        result = session.send_message("Hello")
        
        assert result == "Response message"
        mock_chat.send_message.assert_called_once_with("Hello")
    
    def test_get_history(self):
        """Test getting chat history"""
        mock_history = [
            {"role": "user", "parts": ["Hello"]},
            {"role": "model", "parts": ["Hi there!"]}
        ]
        
        mock_chat = MagicMock()
        mock_chat.history = mock_history
        
        session = ChatSession(mock_chat)
        history = session.get_history()
        
        assert history == mock_history
