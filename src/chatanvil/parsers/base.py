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
