from abc import ABC, abstractmethod
from typing import Dict, List, Any

class BaseConverter(ABC):
    """
    Base class for all format converters
    """
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.format_rules = self._get_format_rules()
    
    @abstractmethod
    def _get_format_rules(self) -> Dict[str, Any]:
        """
        Return the formatting rules for this style
        """
        pass
    
    @abstractmethod
    def convert(self, content: str, metadata: Dict[str, Any], 
                citations: List[Dict[str, Any]], analysis: Dict[str, Any]) -> str:
        """
        Convert the document to the specified format
        """
        pass
    
    def create_title_page(self, metadata: Dict[str, Any]) -> str:
        """
        Create a title page according to the format rules
        """
        pass
    
    def format_headers(self, content: str) -> str:
        """
        Format headers according to the style
        """
        pass
    
    def format_quotes(self, content: str) -> str:
        """
        Format quotations according to the style
        """
        pass
    
    def add_page_numbers(self, content: str) -> str:
        """
        Add page numbers according to the style
        """
        pass
    
    def format_citations(self, content: str, citations: List[Dict[str, Any]]) -> str:
        """
        Format in-text citations according to the style
        """
        pass
    
    def create_references_page(self, citations: List[Dict[str, Any]]) -> str:
        """
        Create the references/works cited page
        """
        pass
