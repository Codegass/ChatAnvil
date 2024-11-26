from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BaseParser(ABC):
    """Base class for response parsers."""
    
    @abstractmethod
    def parse_response(self, response: str) -> str:
        """Parse the response string.
        
        Args:
            response: Raw response string from the model
            
        Returns:
            Parsed response string
        """
        pass
    
    @abstractmethod
    def extract_code(self, response: str) -> List[Dict[str, str]]:
        """Extract code blocks from the response.
        
        Args:
            response: Raw response string from the model
            
        Returns:
            List of dictionaries containing code blocks with language and content
        """
        pass
    
    @abstractmethod
    def format_message(self, message: str, **kwargs: Any) -> str:
        """Format a message before sending to the model.
        
        Args:
            message: Message to format
            **kwargs: Additional formatting options
            
        Returns:
            Formatted message string
        """
        pass
