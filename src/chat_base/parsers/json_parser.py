import json
import re
from typing import Dict, List, Any, Union
from .base import BaseParser

class JSONParser(BaseParser):
    """Parser for JSON formatted responses."""
    
    # 定义可能包含代码的字段名称
    CODE_FIELDS = [
        'code',
        'source',
        'function_code',
        'function',
        'implementation',
        'script'
    ]
    
    def __init__(self):
        self.type = 'json'
        
    def parse_response(self, response: str) -> str:
        """Parse JSON from response, including from markdown code blocks."""
        # First try to extract JSON from markdown code block
        pattern = r'```json\n(.*?)\n```'
        match = re.search(pattern, response, re.DOTALL)
        if match:
            response = match.group(1)
            
        try:
            parsed = json.loads(response)
            return json.dumps(parsed, indent=2)
        except json.JSONDecodeError:
            return response
            
    def _extract_code_recursive(self, data: Union[Dict, List, Any]) -> List[Dict[str, str]]:
        """Recursively extract code blocks from nested JSON structure.
        Only for code blocks in the format of {language: "...", content: "..."}
        
        Args:
            data: JSON data structure (can be dict, list, or primitive type)
            
        Returns:
            List of code blocks found in the structure
        """
        code_blocks = []
        
        if isinstance(data, dict):
            # check if the format is {language: "...", content: "..."}
            if 'content' in data and isinstance(data.get('content'), str):
                language = data.get('language', '')
                code_blocks.append({
                    'language': language,
                    'content': data['content']
                })
                return code_blocks
            
            # Check for code fields at current level
            for field in self.CODE_FIELDS:
                if field in data:
                    code = data[field]
                    if isinstance(code, str):
                        # Try to determine language from context
                        language = data.get('language', '')
                        if not language:
                            # Try to guess language from field name or parent keys
                            if 'python' in field.lower() or 'py' in field.lower():
                                language = 'python'
                            elif 'javascript' in field.lower() or 'js' in field.lower():
                                language = 'javascript'
                            # Add more language detection rules as needed
                        
                        code_blocks.append({
                            'language': language,
                            'content': code
                        })
                    elif isinstance(code, dict):
                        # recursively process nested code objects
                        code_blocks.extend(self._extract_code_recursive(code))
            
            # Recursively check all values
            for value in data.values():
                code_blocks.extend(self._extract_code_recursive(value))
                
        elif isinstance(data, list):
            # Recursively check all items in list
            for item in data:
                code_blocks.extend(self._extract_code_recursive(item))
                
        return code_blocks
            
    def extract_code(self, response: str) -> List[Dict[str, str]]:
        """Extract code blocks from JSON response.
        
        Looks for code blocks in various code-related fields at any nesting level.
        Also handles code blocks in arrays and nested code objects with language/content format.
        
        Returns:
            List of dicts with 'language' and 'content' keys
        """
        code_blocks = []
        try:
            # First try to extract JSON from markdown block
            pattern = r'```json\n(.*?)\n```'
            match = re.search(pattern, response, re.DOTALL)
            if match:
                response = match.group(1)
                
            data = json.loads(response)
            code_blocks = self._extract_code_recursive(data)
                        
        except json.JSONDecodeError:
            pass
            
        return code_blocks 