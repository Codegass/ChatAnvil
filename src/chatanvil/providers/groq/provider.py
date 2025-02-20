from typing import Any, Dict, List, Optional, Union
import groq
from ...providers.base import ChatProvider
from ...utils.logging import ChatLogger
from ...utils.retry import retry_on_rate_limit


class GroqChat(ChatProvider):
    """Groq provider implementation."""

    def __init__(
        self, api_key: Optional[str] = None, model: Optional[str] = None, **kwargs: Any
    ):
        self.logger = ChatLogger("groq")
        self.client = None
        if api_key:
            self.client = groq.Client(api_key=api_key)
        super().__init__(api_key, model)

    def _initialize(self) -> None:
        """Initialize the Groq client."""
        if not self.api_key:
            raise ValueError("Groq API key is required")
        if not self.client:
            self.client = groq.Client(api_key=self.api_key)

    def validate_api_key(self) -> bool:
        """Validate the Groq API key by attempting to create a client."""
        try:
            if not self.api_key:
                return False
            if not self.client:
                self.client = groq.Client(api_key=self.api_key)
            return True
        except Exception as e:
            self.logger.log_error(e, "API key validation failed")
            return False

    @retry_on_rate_limit
    def get_response(
        self,
        message: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.5,
        max_tokens: Optional[int] = 400,
        **kwargs: Any,
    ) -> str:
        """Get a response from Groq."""
        if not self.client:
            raise RuntimeError("Groq client not initialized")

        self.logger.log_request(message, model, system_prompt)

        try:
            messages = []
            if system_prompt or self.system_prompt:
                messages.append(
                    {"role": "system", "content": system_prompt or self.system_prompt}
                )

            messages.append({"role": "user", "content": message})

            response = self.client.chat.completions.create(
                model=model or self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens if max_tokens else None,
            )

            result = response.choices[0].message.content
            self.logger.log_response(result)
            return result

        except Exception as e:
            self.logger.log_response("", error=e)
            raise e

    @retry_on_rate_limit
    def get_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.5,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> str:
        """Get a chat completion from Groq."""
        if not self.client:
            raise RuntimeError("Groq client not initialized")

        try:
            response = self.client.chat.completions.create(
                model=model or self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens if max_tokens else None,
            )

            result = response.choices[0].message.content
            self.logger.log_response(result)
            return result

        except Exception as e:
            self.logger.log_response("", error=e)
            raise e
