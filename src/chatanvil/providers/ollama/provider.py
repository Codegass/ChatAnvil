from typing import Any, Dict, List, Optional, Union
import os
from ollama import Client
from ...providers.base import ChatProvider
from ...utils.logging import ChatLogger
from ...utils.retry import retry_on_rate_limit

class OllamaChat(ChatProvider):
    """Ollama provider implementation using the official Python SDK."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,  # Not used for Ollama
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs: Any
    ):
        self.logger = ChatLogger("ollama")
        self.base_url = base_url or "http://localhost:11434"
        self.client = Client(host=self.base_url)
        super().__init__(api_key, model)
        
    def _initialize(self) -> None:
        """Initialize the Ollama connection."""
        try:
            # Test connection by listing models
            self.client.list()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Ollama: {str(e)}")
    
    def validate_api_key(self) -> bool:
        """Validate the Ollama connection.
        
        Note: Ollama doesn't use API keys, so we just validate the connection.
        """
        try:
            self.client.list()
            return True
        except Exception as e:
            self.logger.error(f"Connection validation failed: {str(e)}")
            return False
    
    @retry_on_rate_limit
    def get_response(
        self,
        message: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ) -> str:
        """Get a response from Ollama using the Python SDK."""
        self.logger.log_request(message, model, system_prompt)
        
        try:
            messages = []
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            messages.append({
                "role": "user",
                "content": message
            })
            
            response = self.client.chat(
                model=model or self.model or "llama3.1",
                messages=messages,
                options={
                    "temperature": temperature,
                    **({"num_predict": max_tokens} if max_tokens else {})
                }
            )
            
            result = response["message"]["content"]
            self.logger.log_response(result)
            return result
            
        except Exception as e:
            self.logger.log_response("", error=e)
            raise e
            
    def get_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ) -> str:
        """Get a chat completion from Ollama using the Python SDK."""
        try:
            response = self.client.chat(
                model=model or self.model or "llama2",
                messages=messages,
                options={
                    "temperature": temperature,
                    **({"num_predict": max_tokens} if max_tokens else {})
                }
            )
            
            result = response["message"]["content"]
            self.logger.log_response(result)
            return result
            
        except Exception as e:
            self.logger.log_response("", error=e)
            raise e
