import re
import xml.etree.ElementTree as ET
from typing import Dict, List
from .base import BaseParser


class XMLParser(BaseParser):
    """Parser for XML formatted responses."""

    def __init__(self):
        self.type = "xml"

    def parse_response(self, response: str) -> str:
        """Parse XML from response, including from markdown code blocks."""
        # First try to extract XML from markdown code block
        pattern = r"```xml\n(.*?)\n```"
        match = re.search(pattern, response, re.DOTALL)
        if match:
            response = match.group(1)

        try:
            root = ET.fromstring(response)
            # Return pretty formatted XML
            from xml.dom import minidom

            xml_str = ET.tostring(root, encoding="unicode")
            return minidom.parseString(xml_str).toprettyxml(indent="  ")
        except ET.ParseError:
            return response

    def extract_code(self, response: str) -> List[Dict[str, str]]:
        """Extract code blocks from XML response.

        Looks for code in <code> or <source> tags.
        """
        code_blocks = []
        try:
            # First try to extract XML from markdown block
            pattern = r"```xml\n(.*?)\n```"
            match = re.search(pattern, response, re.DOTALL)
            if match:
                response = match.group(1)

            root = ET.fromstring(response)

            # Look for code in common XML tags
            for tag in ["code", "source"]:
                for elem in root.findall(f".//{tag}"):
                    code_blocks.append(
                        {
                            "language": elem.get("language", ""),
                            "content": elem.text.strip() if elem.text else "",
                        }
                    )

        except ET.ParseError:
            pass

        return code_blocks
