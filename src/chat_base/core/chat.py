from typing import Any, Dict, List, Optional, Type, Union
from ..providers.base import ChatProvider
from .config import Config

class Chat:
    """Main interface for interacting with chat providers."""
    
    def __init__(
        self,
        service_provider: str,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs: Any
    ):
        self.config = Config(service_provider=service_provider)
        self.provider_name = service_provider.lower()
        
        # Get provider configuration
        provider_config = self.config
        
        # Update with any provided overrides
        if api_key:
            provider_config.api_key = api_key
        if model:
            provider_config.model = model
            
        # Initialize the appropriate provider
        self.provider = self._get_provider_instance(provider_config, **kwargs)
    
    def _get_provider_instance(
        self, 
        config: Config,
        **kwargs: Any
    ) -> ChatProvider:
        """Get the appropriate provider instance based on the service name."""
        # Import providers here to avoid circular imports
        from ..providers.openai import OpenAIChat
        from ..providers.claude import ClaudeChat
        from ..providers.groq import GroqChat
        from ..providers.ollama import OllamaChat
        
        providers: Dict[str, Type[ChatProvider]] = {
            'openai': OpenAIChat,
            'claude': ClaudeChat,
            'groq': GroqChat,
            'ollama': OllamaChat
        }
        
        if self.provider_name not in providers:
            raise ValueError(f"Unsupported provider: {self.provider_name}")
            
        provider_class = providers[self.provider_name]
        return provider_class(
            api_key=config.api_key,
            model=config.model,
            **kwargs
        )
    
    def get_response(
        self,
        message: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ) -> str:
        """Get a response from the chat provider."""
        return self.provider.get_response(
            message=message,
            model=model,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
    
    def get_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ) -> Union[str, Dict[str, Any]]:
        """Get a chat completion from the provider."""
        return self.provider.get_chat_completion(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
    
    def set_system_prompt(self, prompt: str) -> None:
        """Set the system prompt for future conversations."""
        self.provider.set_system_prompt(prompt)
