import re
from typing import Any, Dict, List
from .base import BaseParser

class MarkdownParser(BaseParser):
    """Parser for markdown-formatted responses."""
    
    def __init__(self):
        # Regex pattern for code blocks
        self.code_pattern = re.compile(
            r'```(\w+)?\n(.*?)\n```',
            re.DOTALL
        )
    
    def parse_response(self, response: str) -> str:
        """Parse markdown-formatted response.
        
        Handles:
        - Code blocks with language specification
        - Inline code
        - Headers
        - Lists
        """
        # Remove any trailing whitespace
        response = response.strip()
        
        # Ensure code blocks are properly formatted
        response = self._normalize_code_blocks(response)
        
        return response
    
    def extract_code(self, response: str) -> List[Dict[str, str]]:
        """Extract code blocks from markdown response.
        
        Returns:
            List of dictionaries with 'language' and 'code' keys
        """
        code_blocks = []
        
        for match in self.code_pattern.finditer(response):
            language = match.group(1) or 'text'
            code = match.group(2).strip()
            
            code_blocks.append({
                'language': language,
                'code': code
            })
            
        return code_blocks
    
    def format_message(self, message: str, **kwargs: Any) -> str:
        """Format a message in markdown.
        
        Args:
            message: Message to format
            **kwargs: Additional formatting options
                code_language: Default language for code blocks
                
        Returns:
            Markdown-formatted message
        """
        code_language = kwargs.get('code_language', 'python')
        
        # Wrap code blocks that don't have language specified
        def replace_code_block(match):
            if match.group(1):  # Language is specified
                return match.group(0)
            return f'```{code_language}\n{match.group(2)}\n```'
            
        message = self.code_pattern.sub(replace_code_block, message)
        
        return message
    
    def _normalize_code_blocks(self, text: str) -> str:
        """Ensure code blocks are properly formatted.
        
        - Add missing language identifiers
        - Ensure proper spacing around code blocks
        """
        # Ensure empty lines around code blocks
        text = re.sub(r'([^\n])(```)', r'\1\n```', text)
        text = re.sub(r'(```\w*\n.*?\n```)([^\n])', r'\1\n\2', text, flags=re.DOTALL)
        
        return text
