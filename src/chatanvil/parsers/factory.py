from typing import Optional, Type
from .base import BaseParser
from .default import DefaultParser
from .markdown import MarkdownParser
from .json_parser import JSONParser
from .xml_parser import XMLParser

class ParserFactory:
    """Factory for creating response parsers."""
    
    _parsers = {
        'default': DefaultParser,
        'markdown': MarkdownParser,
        'json': JSONParser,
        'xml': XMLParser
    }
    
    @classmethod
    def get_parser(cls, parser_type: str = 'default') -> BaseParser:
        """Get a parser instance by type.
        
        Args:
            parser_type: Type of parser to create ('default', 'markdown', 'json', 'xml')
            
        Returns:
            Instance of the requested parser
            
        Raises:
            ValueError: If parser_type is not supported
        """
        parser_class = cls._parsers.get(parser_type.lower())
        if not parser_class:
            raise ValueError(
                f"Unsupported parser type: {parser_type}. "
                f"Available types: {', '.join(cls._parsers.keys())}"
            )
        return parser_class()
    
    @classmethod
    def register_parser(
        cls,
        parser_type: str,
        parser_class: Type[BaseParser]
    ) -> None:
        """Register a new parser type.
        
        Args:
            parser_type: Name of the parser type
            parser_class: Parser class to register
            
        Raises:
            TypeError: If parser_class is not a subclass of BaseParser
        """
        if not issubclass(parser_class, BaseParser):
            raise TypeError(
                f"Parser class must be a subclass of BaseParser, "
                f"got {parser_class.__name__}"
            )
        cls._parsers[parser_type.lower()] = parser_class
