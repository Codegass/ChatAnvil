from typing import Any, Dict, List, Optional, Union
import groq
from ...providers.base import ChatProvider
from ...utils.logging import ChatLogger
from ...utils.retry import retry_on_rate_limit

class GroqChat(ChatProvider):
    """Groq provider implementation."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs: Any
    ):
        super().__init__(api_key, model)
        self.logger = ChatLogger("groq")
        self.client: Optional[groq.Client] = None
        
    def _initialize(self) -> None:
        """Initialize the Groq client."""
        if not self.api_key:
            raise ValueError("Groq API key is required")
        self.client = groq.Client(api_key=self.api_key)
    
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
        """Get a response from Groq."""
        if not self.client:
            raise RuntimeError("Groq client not initialized")
            
        self.logger.log_request(message, model, system_prompt)
        
        try:
            messages = []
            if system_prompt or self.system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt or self.system_prompt
                })
            
            messages.append({
                "role": "user",
                "content": message
            })
            
            response = self.client.chat.completions.create(
                model=model or self.model or "mixtral-8x7b-32768",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            result = response.choices[0].message.content
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
        """Get a chat completion from Groq."""
        if not self.client:
            raise RuntimeError("Groq client not initialized")
            
        try:
            response = self.client.chat.completions.create(
                model=model or self.model or "mixtral-8x7b-32768",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.log_error(e, "Chat completion failed")
            raise
    
    def validate_api_key(self) -> bool:
        """Validate the Groq API key."""
        if not self.client:
            return False
            
        try:
            # Make a minimal API call to validate the key
            self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=1
            )
            return True
        except Exception as e:
            self.logger.log_error(e, "API key validation failed")
            return False
