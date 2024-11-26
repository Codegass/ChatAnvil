import re
import xml.etree.ElementTree as ET
from typing import Any, Dict, List
from xml.dom import minidom
from .base import BaseParser

class XMLParser(BaseParser):
    """Parser for XML-formatted responses."""
    
    def __init__(self):
        self.code_pattern = re.compile(
            r'```(\w+)?\n(.*?)\n```',
            re.DOTALL
        )
    
    def parse_response(self, response: str) -> str:
        """Parse XML-formatted response.
        
        Attempts to:
        1. Parse the entire response as XML
        2. Extract XML elements from markdown-like responses
        3. Return the original response if no valid XML is found
        """
        # Try to find XML content
        xml_pattern = r'<\?xml.*?\?>.*?</\w+>|<\w+>.*?</\w+>'
        matches = re.finditer(xml_pattern, response, re.DOTALL)
        
        for match in matches:
            try:
                xml_str = match.group(0)
                # Parse and pretty print the XML
                parsed = minidom.parseString(xml_str)
                formatted_xml = parsed.toprettyxml(indent="  ")
                # Remove empty lines
                formatted_xml = '\n'.join(
                    line for line in formatted_xml.split('\n')
                    if line.strip()
                )
                # Replace the original XML with the formatted version
                response = response.replace(xml_str, formatted_xml)
            except Exception:
                continue
        
        return response
    
    def extract_code(self, response: str) -> List[Dict[str, str]]:
        """Extract code blocks and XML content from the response."""
        code_blocks = []
        
        # Extract code blocks
        for match in self.code_pattern.finditer(response):
            language = match.group(1) or 'xml'
            code = match.group(2).strip()
            
            code_blocks.append({
                'language': language,
                'code': code
            })
        
        # Look for XML outside code blocks
        cleaned_response = self.code_pattern.sub('', response)
        xml_pattern = r'<\?xml.*?\?>.*?</\w+>|<\w+>.*?</\w+>'
        matches = re.finditer(xml_pattern, cleaned_response, re.DOTALL)
        
        for match in matches:
            try:
                xml_str = match.group(0)
                # Validate it's valid XML
                ET.fromstring(xml_str)
                code_blocks.append({
                    'language': 'xml',
                    'code': xml_str
                })
            except Exception:
                continue
        
        return code_blocks
    
    def format_message(self, message: str, **kwargs: Any) -> str:
        """Format a message for XML output.
        
        Args:
            message: Message to format
            **kwargs: Additional formatting options
                root_tag: Root element tag name (default: 'message')
                add_header: Whether to add XML declaration (default: True)
                
        Returns:
            XML-formatted message
        """
        root_tag = kwargs.get('root_tag', 'message')
        add_header = kwargs.get('add_header', True)
        
        try:
            # Check if the message is already XML
            ET.fromstring(message)
            return message
        except Exception:
            # Create a new XML document
            root = ET.Element(root_tag)
            root.text = message
            
            # Convert to string
            xml_str = ET.tostring(root, encoding='unicode')
            
            if add_header:
                xml_str = f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_str}'
            
            # Pretty print
            try:
                parsed = minidom.parseString(xml_str)
                formatted_xml = parsed.toprettyxml(indent="  ")
                # Remove empty lines
                formatted_xml = '\n'.join(
                    line for line in formatted_xml.split('\n')
                    if line.strip()
                )
                return formatted_xml
            except Exception:
                return xml_str
