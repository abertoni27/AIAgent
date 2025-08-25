from .base_converter import BaseConverter
from typing import Dict, List, Any
from citation_manager import CitationManager
import re

class IEEEConverter(BaseConverter):
    """
    IEEE (Institute of Electrical and Electronics Engineers) format converter
    """
    
    def _get_format_rules(self) -> Dict[str, Any]:
        return {
            'name': 'IEEE',
            'margins': '1 inch on all sides',
            'spacing': 'Single-spaced',
            'font': 'Times New Roman, 10pt',
            'header': 'Title and page number',
            'title_format': 'Centered, bold',
            'indentation': '0.5 inch for paragraphs',
            'quotes': 'Double quotes for short quotes, block quotes for 40+ words',
            'citations': 'Numbered references in brackets',
            'references': 'Separate page, numbered list'
        }
    
    def convert(self, content: str, metadata: Dict[str, Any], 
                citations: List[Dict[str, Any]], analysis: Dict[str, Any]) -> str:
        """
        Convert document to IEEE format
        """
        formatted_doc = ""
        
        # Add title page
        formatted_doc += self.create_title_page(metadata)
        formatted_doc += "\n\n"
        
        # Add abstract if not present
        if not self._has_abstract(content):
            formatted_doc += self._create_abstract(content)
            formatted_doc += "\n\n"
        
        # Format the main content
        formatted_content = self._format_content(content, citations)
        formatted_doc += formatted_content
        
        # Add references page
        if citations:
            formatted_doc += "\n\n"
            formatted_doc += self.create_references_page(citations)
        
        return formatted_doc
    
    def create_title_page(self, metadata: Dict[str, Any]) -> str:
        """
        Create IEEE title page
        """
        title_page = ""
        
        # Title (centered, bold)
        if metadata.get('title'):
            title_page += f"{metadata['title']}\n\n"
        
        # Author information (centered)
        if metadata.get('author'):
            title_page += f"{metadata['author']}\n\n"
        
        # Course information
        if metadata.get('course'):
            title_page += f"{metadata['course']}\n"
        
        if metadata.get('instructor'):
            title_page += f"{metadata['instructor']}\n"
        
        if metadata.get('due_date'):
            title_page += f"{metadata['due_date']}\n"
        
        return title_page
    
    def _has_abstract(self, content: str) -> bool:
        """
        Check if content has an abstract
        """
        return 'abstract' in content.lower()[:500]  # Check first 500 characters
    
    def _create_abstract(self, content: str) -> str:
        """
        Create an abstract from the content
        """
        # Extract first paragraph or first few sentences as abstract
        paragraphs = content.split('\n\n')
        if paragraphs:
            first_paragraph = paragraphs[0]
            sentences = re.split(r'[.!?]+', first_paragraph)
            
            # Take first 2-3 sentences for abstract
            abstract_sentences = sentences[:3]
            abstract = '. '.join(abstract_sentences) + '.'
            
            return f"Abstract—{abstract}"
        
        return "Abstract—[Abstract content would be generated here]"
    
    def _format_content(self, content: str, citations: List[Dict[str, Any]]) -> str:
        """
        Format the main content according to IEEE rules
        """
        # Split into paragraphs
        paragraphs = content.split('\n\n')
        formatted_paragraphs = []
        
        for paragraph in paragraphs:
            if paragraph.strip():
                # Format citations in the paragraph
                formatted_paragraph = self._format_citations_in_text(paragraph, citations)
                
                # Add proper indentation
                formatted_paragraph = "    " + formatted_paragraph.strip()
                formatted_paragraphs.append(formatted_paragraph)
        
        return "\n\n".join(formatted_paragraphs)
    
    def _format_citations_in_text(self, text: str, citations: List[Dict[str, Any]]) -> str:
        """
        Format citations within text according to IEEE style
        """
        # Replace existing citations with IEEE format
        for i, citation in enumerate(citations):
            citation_text = citation.get('text', '')
            if citation_text in text:
                ieee_citation = self._format_ieee_citation(citation, i + 1)
                text = text.replace(citation_text, ieee_citation)
        
        return text
    
    def _format_ieee_citation(self, citation: Dict[str, Any], number: int) -> str:
        """
        Format a single citation in IEEE style
        """
        return f"[{number}]"
    
    def format_quotes(self, content: str) -> str:
        """
        Format quotations according to IEEE style
        """
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            # Check for quotes in the line
            if '"' in line or "'" in line:
                # Format as short quote with proper indentation
                line = self._format_short_quote(line)
            formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def _format_short_quote(self, line: str) -> str:
        """
        Format a short quote according to IEEE style
        """
        # Ensure proper quote formatting
        # Replace straight quotes with curly quotes if needed
        line = line.replace('"', '"').replace('"', '"')
        line = line.replace("'", "'").replace("'", "'")
        
        return line
    
    def add_page_numbers(self, content: str) -> str:
        """
        Add page numbers in IEEE format
        """
        lines = content.split('\n')
        page_number = 1
        formatted_lines = []
        
        for i, line in enumerate(lines):
            formatted_lines.append(line)
            
            # Add page number every 25 lines (approximate page break)
            if i > 0 and i % 25 == 0:
                formatted_lines.append(f"\n{page_number}\n")
                page_number += 1
        
        return '\n'.join(formatted_lines)
    
    def create_references_page(self, citations: List[Dict[str, Any]]) -> str:
        """
        Create IEEE reference list
        """
        citation_manager = CitationManager()
        return citation_manager.generate_works_cited(citations, 'ieee')
    
    def format_headers(self, content: str) -> str:
        """
        Format headers according to IEEE style
        """
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            # Check if line is a header
            if self._is_header(line):
                # Format as IEEE header (centered, bold)
                formatted_lines.append(f"\n{line.strip()}\n")
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def _is_header(self, line: str) -> bool:
        """
        Check if a line is a header
        """
        line = line.strip()
        if not line:
            return False
        
        # Check for common header patterns
        header_patterns = [
            r'^[A-Z\s]+$',  # All caps
            r'^\d+\.\s+[A-Z]',  # Numbered sections
            r'^[A-Z][a-z]+(\s+[A-Z][a-z]+)*$'  # Title case
        ]
        
        return any(re.match(pattern, line) for pattern in header_patterns)
