from typing import Any, Dict, List
from .base import BaseParser

class DefaultParser(BaseParser):
    """Default parser that returns responses as-is."""
    
    def parse_response(self, response: str) -> str:
        """Return the response without modification."""
        return response
    
    def extract_code(self, response: str) -> List[Dict[str, str]]:
        """No code extraction in default parser."""
        return []
    
    def format_message(self, message: str, **kwargs: Any) -> str:
        """Return the message without modification."""
        return message
