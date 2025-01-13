import re
from typing import Dict, List
from .base import BaseParser

class MarkdownParser(BaseParser):
    """Parser for markdown formatted responses."""
    
    def __init__(self):
        self.type = 'markdown'
        
    def parse_response(self, response: str) -> str:
        """Return the response with markdown formatting intact."""
        return response
        
    def extract_code(self, response: str) -> List[Dict[str, str]]:
        """Extract code blocks from markdown response.
        
        Returns:
            List of dicts with 'language' and 'content' keys
        """
        code_blocks = []
        pattern = r'```(\w+)?\n(.*?)\n```'
        matches = re.finditer(pattern, response, re.DOTALL)
        
        for match in matches:
            language = match.group(1) or ''
            content = match.group(2).strip()
            code_blocks.append({
                'language': language,
                'content': content
            })
            
        return code_blocks 