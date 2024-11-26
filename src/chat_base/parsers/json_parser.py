import json
import re
from typing import Any, Dict, List
from .base import BaseParser

class JSONParser(BaseParser):
    """Parser for JSON-formatted responses."""
    
    def __init__(self):
        self.code_pattern = re.compile(
            r'```(\w+)?\n(.*?)\n```',
            re.DOTALL
        )
    
    def parse_response(self, response: str) -> str:
        """Parse JSON-formatted response.
        
        Attempts to:
        1. Parse the entire response as JSON
        2. Extract JSON objects from markdown-like responses
        3. Return the original response if no JSON is found
        """
        try:
            # Try parsing the entire response as JSON
            parsed = json.loads(response)
            return json.dumps(parsed, indent=2)
        except json.JSONDecodeError:
            # Look for JSON objects in the response
            json_pattern = r'\{[^{}]*\}'
            matches = re.finditer(json_pattern, response)
            
            for match in matches:
                try:
                    json_str = match.group(0)
                    parsed = json.loads(json_str)
                    # Replace the JSON string with a properly formatted version
                    response = response.replace(
                        json_str,
                        json.dumps(parsed, indent=2)
                    )
                except json.JSONDecodeError:
                    continue
            
            return response
    
    def extract_code(self, response: str) -> List[Dict[str, str]]:
        """Extract code blocks from the response.
        
        Also attempts to parse JSON objects outside of code blocks.
        """
        code_blocks = []
        
        # Extract code blocks
        for match in self.code_pattern.finditer(response):
            language = match.group(1) or 'json'
            code = match.group(2).strip()
            
            code_blocks.append({
                'language': language,
                'code': code
            })
        
        # Look for JSON objects outside code blocks
        cleaned_response = self.code_pattern.sub('', response)
        json_pattern = r'\{[^{}]*\}'
        matches = re.finditer(json_pattern, cleaned_response)
        
        for match in matches:
            try:
                json_str = match.group(0)
                json.loads(json_str)  # Validate it's valid JSON
                code_blocks.append({
                    'language': 'json',
                    'code': json_str
                })
            except json.JSONDecodeError:
                continue
        
        return code_blocks
    
    def format_message(self, message: str, **kwargs: Any) -> str:
        """Format a message for JSON output.
        
        Args:
            message: Message to format
            **kwargs: Additional formatting options
                wrap_json: Whether to wrap non-JSON messages in a JSON object
                
        Returns:
            JSON-formatted message
        """
        wrap_json = kwargs.get('wrap_json', True)
        
        try:
            # Check if the message is already JSON
            json.loads(message)
            return message
        except json.JSONDecodeError:
            if wrap_json:
                # Wrap non-JSON messages in a JSON object
                return json.dumps({
                    "message": message
                }, indent=2)
            return message
