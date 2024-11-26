import logging
import os
from datetime import datetime
from typing import Optional
from ..core.config import Config

class ChatLogger:
    """Logger for chat interactions."""
    
    def __init__(self, provider: str):
        self.config = Config()
        self.provider = provider
        
        # Create logs directory if it doesn't exist
        os.makedirs(self.config.log_dir, exist_ok=True)
        
        # Set up logging
        self.logger = logging.getLogger(f"chat_base.{provider}")
        self.logger.setLevel(logging.DEBUG if self.config.debug else logging.INFO)
        
        # File handler
        log_file = os.path.join(
            self.config.log_dir,
            f"{provider}_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        self.logger.addHandler(file_handler)
        
        # Console handler if debug is enabled
        if self.config.debug:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(
                logging.Formatter('%(name)s - %(levelname)s - %(message)s')
            )
            self.logger.addHandler(console_handler)
    
    def log_request(
        self,
        message: str,
        model: Optional[str],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> None:
        """Log an API request."""
        self.logger.info(
            f"Request - Model: {model}, Message: {message[:100]}..."
            + (f", System Prompt: {system_prompt[:100]}..." if system_prompt else "")
        )
        if self.config.debug:
            self.logger.debug(f"Full kwargs: {kwargs}")
    
    def log_response(self, response: str, error: Optional[Exception] = None) -> None:
        """Log an API response."""
        if error:
            self.logger.error(f"Error: {str(error)}")
        else:
            self.logger.info(f"Response: {response[:100]}...")
            if self.config.debug:
                self.logger.debug(f"Full response: {response}")
    
    def log_error(self, error: Exception, context: Optional[str] = None) -> None:
        """Log an error with optional context."""
        if context:
            self.logger.error(f"{context}: {str(error)}")
        else:
            self.logger.error(str(error))
