from typing import Any, Dict, List
from .base import BaseParser


class DefaultParser(BaseParser):
    """Default parser that returns responses as-is."""

    def __init__(self):
        self.type = "default"

    def parse_response(self, response: str) -> str:
        """Return the response without modification."""
        return response

    def extract_code(self, response: str) -> List[Dict[str, str]]:
        """No code extraction in default parser."""
        return []
