import logging
import os
from datetime import datetime
from typing import Optional, Dict
from ..core.config import Config


class ChatLogger:
    """Logger for chat interactions."""

    def __init__(self, provider_name: str):
        """Initialize the logger with provider-specific configuration.

        Args:
            provider_name (str): The service provider name (e.g., 'openai', 'claude')
        """
        self.config = Config(service_provider=provider_name)
        self.provider = provider_name
        self._system_prompt_logged = False

        # Set up main logger
        self.logger = logging.getLogger(f"chatanvil.{provider_name}")
        # 确保只添加一次handler
        if not self.logger.handlers:  
            self._setup_handlers()

        # Set up chat logger for conversation history
        self.chat_logger = logging.getLogger(f"chatanvil.{provider_name}.chat")
        self.chat_logger.setLevel(logging.INFO)

        # Create chat log file with provider, model, and timestamp
        if self.config.log_dir:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            chat_filename = f"{provider_name}_{self.transform_file_name_from_slash_to_dot(self.config.model)}_{timestamp}.chat"
            chat_log_dir = os.path.join(self.config.log_dir, "chats")
            os.makedirs(chat_log_dir, exist_ok=True)

            chat_handler = logging.FileHandler(
                os.path.join(chat_log_dir, chat_filename)
            )
            chat_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
            self.chat_logger.addHandler(chat_handler)

            # Log initial chat session information
            self.chat_logger.info("=== Chat Session Started ===")
            self.chat_logger.info(f"Provider: {provider_name}")
            self.chat_logger.info(f"Model: {self.transform_file_name_from_slash_to_dot(self.config.model)}")
            self.chat_logger.info("-" * 50)

    def _setup_handlers(self):
        """配置日志处理器"""
        self.logger.setLevel(logging.DEBUG)
        
        # 控制台handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 文件handler（示例）
        file_handler = logging.FileHandler('chat.log')
        file_handler.setLevel(logging.DEBUG)
        
        # 统一格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def debug(self, message: str) -> None:
        """Log a debug message."""
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """Log an info message."""
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """Log a warning message."""
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """Log an error message."""
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """Log a critical message."""
        self.logger.critical(message)

    def log_error(self, error: Exception, message: Optional[str] = None) -> None:
        """Log an error with optional context message.

        Args:
            error: The exception that occurred
            message: Optional context message to include with the error
        """
        error_msg = f"{message + ': ' if message else ''}{str(error)}"
        self.logger.error(error_msg)

        # Log error details to chat history if available
        if hasattr(self, "chat_logger"):
            self.chat_logger.error(error_msg)

    def log_request(
        self,
        message: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Log a chat request to the conversation history.

        Args:
            message: The user's message
            model: The model being used (if different from config)
            system_prompt: Optional system prompt
            **kwargs: Additional request parameters
        """
        # Log to main logger
        # self.logger.info(f"Request - Model: {model or self.config.model}")
        # if self.config.debug:
        #     self.logger.debug(f"Message: {message}")
            # if system_prompt:
            #     self.logger.debug(f"System Prompt: {system_prompt}")
            # self.logger.debug(f"Additional params: {kwargs}")

        # Log system prompt and parameters only once at the beginning
        if not self._system_prompt_logged:
            if system_prompt:
                self.chat_logger.info("=== System Configuration ===")
                self.chat_logger.info(f"[System Prompt] {system_prompt}")
            if kwargs:
                self.chat_logger.info(f"[Parameters] {kwargs}")
            if system_prompt or kwargs:
                self.chat_logger.info("-" * 50)
            self._system_prompt_logged = True

        # Log the user message
        self.chat_logger.info("[User] " + message)

    def log_response(
        self,
        response: str,
        error: Optional[Exception] = None,
        metadata: Optional[Dict] = None,
    ) -> None:
        """Log a chat response to the conversation history.

        Args:
            response: The model's response
            error: Optional error that occurred
            metadata: Optional response metadata (tokens, finish reason, etc.)
        """
        # Log to main logger
        # if error:
        #     self.logger.error(f"Error in response: {str(error)}")
        # else:
        #     self.logger.info("Response received")
        #     if self.config.debug:
        #         self.logger.debug(f"Response: {response}")
        #         if metadata:
        #             self.logger.debug(f"Metadata: {metadata}")

        # Log to chat history
        if error:
            self.chat_logger.info(f"[Error] {str(error)}")
        else:
            self.chat_logger.info(f"[Assistant] {response}")
            if metadata and self.config.debug:
                self.chat_logger.info(f"[Metadata] {metadata}")
        self.chat_logger.info("-" * 50)

    def transform_file_name_from_slash_to_dot(self, file_name: str) -> str:
        """Transform file name from slash to dot."""
        return file_name.replace("/", ".")
