from typing import Any, Dict, List, Optional, Union
import json
import requests
from ...providers.base import ChatProvider
from ...utils.logging import ChatLogger
from ...utils.retry import retry_on_rate_limit

class OllamaChat(ChatProvider):
    """Ollama provider implementation."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,  # Not used for Ollama
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs: Any
    ):
        super().__init__(api_key, model)
        self.logger = ChatLogger("ollama")
        self.base_url = base_url or "http://localhost:11434"
        
    def _initialize(self) -> None:
        """Initialize the Ollama connection."""
        # Validate the base URL is accessible
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code != 200:
                raise ConnectionError(f"Failed to connect to Ollama: {response.text}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Ollama: {str(e)}")
    
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
        """Get a response from Ollama."""
        self.logger.log_request(message, model, system_prompt)
        
        try:
            # Prepare the request
            url = f"{self.base_url}/api/chat"
            data = {
                "model": model or self.model or "llama2",
                "messages": [],
                "options": {
                    "temperature": temperature,
                }
            }
            
            if max_tokens:
                data["options"]["num_predict"] = max_tokens
                
            if system_prompt or self.system_prompt:
                data["messages"].append({
                    "role": "system",
                    "content": system_prompt or self.system_prompt
                })
            
            data["messages"].append({
                "role": "user",
                "content": message
            })
            
            # Make the request
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()["message"]["content"]
            self.logger.log_response(result)
            return result
            
        except Exception as e:
            self.logger.log_response("", error=e)
            raise
    
    @retry_on_rate_limit
    def get_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ) -> Union[str, Dict[str, Any]]:
        """Get a chat completion from Ollama."""
        try:
            url = f"{self.base_url}/api/chat"
            data = {
                "model": model or self.model or "llama2",
                "messages": messages,
                "options": {
                    "temperature": temperature,
                }
            }
            
            if max_tokens:
                data["options"]["num_predict"] = max_tokens
            
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            return response.json()["message"]["content"]
            
        except Exception as e:
            self.logger.log_error(e, "Chat completion failed")
            raise
    
    def validate_api_key(self) -> bool:
        """Validate the Ollama connection."""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except Exception as e:
            self.logger.log_error(e, "Connection validation failed")
            return False
