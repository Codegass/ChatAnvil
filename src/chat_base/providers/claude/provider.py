from typing import Any, Dict, List, Optional, Union
import anthropic
from ...providers.base import ChatProvider
from ...utils.logging import ChatLogger
from ...utils.retry import retry_on_rate_limit

class ClaudeChat(ChatProvider):
    """Anthropic Claude provider implementation."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs: Any
    ):
        super().__init__(api_key, model)
        self.logger = ChatLogger("claude")
        self.client: Optional[anthropic.Client] = None
        
    def _initialize(self) -> None:
        """Initialize the Claude client."""
        if not self.api_key:
            raise ValueError("Claude API key is required")
        self.client = anthropic.Client(api_key=self.api_key)
    
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
        """Get a response from Claude."""
        if not self.client:
            raise RuntimeError("Claude client not initialized")
            
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
            
            response = self.client.messages.create(
                model=model or self.model or "claude-3-opus-20240229",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            result = response.content[0].text
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
        """Get a chat completion from Claude."""
        if not self.client:
            raise RuntimeError("Claude client not initialized")
            
        try:
            response = self.client.messages.create(
                model=model or self.model or "claude-3-opus-20240229",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            return response.content[0].text
            
        except Exception as e:
            self.logger.log_error(e, "Chat completion failed")
            raise
    
    def validate_api_key(self) -> bool:
        """Validate the Claude API key."""
        if not self.client:
            return False
            
        try:
            # Make a minimal API call to validate the key
            self.client.messages.create(
                model="claude-3-opus-20240229",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=1
            )
            return True
        except Exception as e:
            self.logger.log_error(e, "API key validation failed")
            return False
