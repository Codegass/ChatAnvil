from typing import Any, Dict, List, Optional
import anthropic
from ...providers.base import ChatProvider
from ...utils.logging import ChatLogger
from ...utils.retry import retry_on_rate_limit


class ClaudeChat(ChatProvider):
    """Anthropic Claude provider implementation."""

    def __init__(
        self, api_key: Optional[str] = None, model: Optional[str] = None, **kwargs: Any
    ):
        self.logger = ChatLogger("claude")
        self.client = None
        if api_key:
            self.client = anthropic.Client(api_key=api_key)
        super().__init__(api_key, model)

    def _initialize(self) -> None:
        """Initialize the Claude client."""
        if not self.api_key:
            raise ValueError("Claude API key is required")
        if not self.client:
            self.client = anthropic.Client(api_key=self.api_key)

    def validate_api_key(self) -> bool:
        """Validate the Claude API key by attempting to create a client."""
        try:
            if not self.api_key:
                return False
            if not self.client:
                self.client = anthropic.Client(api_key=self.api_key)
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
        temperature: float = 0.7,
        max_tokens: Optional[int] = 4000,
        **kwargs: Any,
    ) -> str:
        """Get a response from Claude."""
        if not self.client:
            raise RuntimeError("Claude client not initialized")

        self.logger.log_request(message, model, system_prompt)

        try:
            # Claude API expects system prompt as a top-level parameter
            response = self.client.messages.create(
                model=model or self.model,
                system=system_prompt
                or self.system_prompt,  # Pass system prompt directly
                messages=[{"role": "user", "content": message}],
                temperature=temperature,
                max_tokens=max_tokens if max_tokens else 4000,
            )

            result = response.content[0].text
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
        temperature: float = 0.7,
        max_tokens: Optional[int] = 4000,
        **kwargs: Any,
    ) -> str:
        """Get a chat completion from Claude."""
        if not self.client:
            raise RuntimeError("Claude client not initialized")

        try:
            # Extract system message if present
            system_message = None
            chat_messages = []

            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    chat_messages.append(msg)

            response = self.client.messages.create(
                model=model or self.model,
                system=system_message,  # Pass system message as top-level parameter
                messages=chat_messages,
                temperature=temperature,
                max_tokens=max_tokens if max_tokens else 4000,
            )

            result = response.content[0].text
            self.logger.log_response(result)
            return result

        except Exception as e:
            self.logger.log_response("", error=e)
            raise e
