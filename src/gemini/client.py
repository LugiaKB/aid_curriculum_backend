"""
Gemini API Client

This module provides a client for interacting with Google's Gemini API.
"""

import os
from typing import Optional, Dict, Any, List
import google.generativeai as genai


class GeminiClient:
    """
    Client for interacting with Google's Gemini API.
    
    This client handles authentication and basic API communication
    with the Gemini generative AI service.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gemini-pro"
    ):
        """
        Initialize the Gemini client.
        
        Args:
            api_key: Gemini API key. If not provided, will look for GEMINI_API_KEY env var.
            model_name: Name of the Gemini model to use (default: gemini-pro).
        
        Raises:
            ValueError: If no API key is provided or found in environment.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Gemini API key must be provided either as parameter or "
                "through GEMINI_API_KEY environment variable"
            )
        
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-pro")
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel(self.model_name)
    
    def generate_content(
        self,
        prompt: str,
        **kwargs: Any
    ) -> str:
        """
        Generate content using the Gemini model.
        
        Args:
            prompt: The prompt to send to the model.
            **kwargs: Additional parameters to pass to the generation method.
        
        Returns:
            Generated text response from the model.
        
        Raises:
            Exception: If the API call fails.
        """
        try:
            response = self.model.generate_content(prompt, **kwargs)
            return response.text
        except Exception as e:
            raise Exception(f"Failed to generate content: {str(e)}")
    
    def generate_content_stream(
        self,
        prompt: str,
        **kwargs: Any
    ):
        """
        Generate content using streaming response.
        
        Args:
            prompt: The prompt to send to the model.
            **kwargs: Additional parameters to pass to the generation method.
        
        Yields:
            Chunks of generated text from the model.
        
        Raises:
            Exception: If the API call fails.
        """
        try:
            response = self.model.generate_content(prompt, stream=True, **kwargs)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            raise Exception(f"Failed to generate streaming content: {str(e)}")
    
    def chat(
        self,
        history: Optional[List[Dict[str, str]]] = None
    ) -> "ChatSession":
        """
        Start a chat session.
        
        Args:
            history: Optional chat history to initialize the session with.
        
        Returns:
            A ChatSession object for maintaining conversation context.
        """
        chat = self.model.start_chat(history=history or [])
        return ChatSession(chat)


class ChatSession:
    """
    Wrapper for Gemini chat session to maintain conversation context.
    """
    
    def __init__(self, chat):
        """
        Initialize the chat session.
        
        Args:
            chat: The underlying Gemini chat object.
        """
        self.chat = chat
    
    def send_message(self, message: str, **kwargs: Any) -> str:
        """
        Send a message in the chat session.
        
        Args:
            message: The message to send.
            **kwargs: Additional parameters for the message.
        
        Returns:
            The model's response text.
        
        Raises:
            Exception: If sending the message fails.
        """
        try:
            response = self.chat.send_message(message, **kwargs)
            return response.text
        except Exception as e:
            raise Exception(f"Failed to send message: {str(e)}")
    
    def get_history(self) -> List[Dict[str, str]]:
        """
        Get the chat history.
        
        Returns:
            List of message dictionaries containing the conversation history.
        """
        return self.chat.history
