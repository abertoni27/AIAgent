import re
import openai
import os
from typing import Dict, List, Any
from format_converters.mla_converter import MLAConverter
from format_converters.apa_converter import APAConverter
from format_converters.chicago_converter import ChicagoConverter
from format_converters.harvard_converter import HarvardConverter
from format_converters.ieee_converter import IEEEConverter
from citation_manager import CitationManager

class DocumentProcessor:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.citation_manager = CitationManager()
        
        # Initialize format converters
        self.converters = {
            'mla': MLAConverter(),
            'apa': APAConverter(),
            'chicago': ChicagoConverter(),
            'harvard': HarvardConverter(),
            'ieee': IEEEConverter()
        }
    
    def format_document(self, content: str, format_type: str, metadata: Dict[str, Any]) -> str:
        """
        Format a document according to the specified academic format
        """
        try:
            # Get the appropriate converter
            converter = self.converters.get(format_type)
            if not converter:
                raise ValueError(f"Unsupported format: {format_type}")
            
            # Analyze document structure
            analysis = self._analyze_document_structure(content)
            
            # Extract and process citations
            citations = self.citation_manager.extract_citations(content)
            
            # Format the document
            formatted_doc = converter.convert(
                content=content,
                metadata=metadata,
                citations=citations,
                analysis=analysis
            )
            
            return formatted_doc
            
        except Exception as e:
            raise Exception(f"Error formatting document: {str(e)}")
    
    def analyze_missing_information(self, content: str, format_type: str) -> List[str]:
        """
        Analyze the document for missing information required for proper formatting
        """
        missing_info = []
        
        # Check for basic document elements
        if not self._has_title_page_info(content):
            missing_info.append("Title page information (title, author, course, instructor, date)")
        
        if not self._has_abstract(content):
            if format_type in ['apa', 'ieee']:
                missing_info.append("Abstract section")
        
        if not self._has_introduction(content):
            missing_info.append("Introduction section")
        
        if not self._has_conclusion(content):
            missing_info.append("Conclusion section")
        
        # Check for citations
        citations = self.citation_manager.extract_citations(content)
        if not citations:
            missing_info.append("Citations and references")
        
        # Check for specific format requirements
        if format_type == 'mla':
            if not self._has_works_cited(content):
                missing_info.append("Works Cited page")
        
        elif format_type == 'apa':
            if not self._has_references(content):
                missing_info.append("References page")
            if not self._has_running_head(content):
                missing_info.append("Running head")
        
        elif format_type == 'chicago':
            if not self._has_footnotes(content) and not self._has_bibliography(content):
                missing_info.append("Footnotes or bibliography")
        
        elif format_type == 'ieee':
            if not self._has_numbered_references(content):
                missing_info.append("Numbered reference list")
        
        # Check for quotes
        if not self._has_proper_quotes(content):
            missing_info.append("Properly formatted quotations")
        
        # Check for page numbers
        if not self._has_page_numbers(content):
            missing_info.append("Page numbering")
        
        return missing_info
    
    def _analyze_document_structure(self, content: str) -> Dict[str, Any]:
        """
        Analyze the structure of the document
        """
        analysis = {
            'sections': [],
            'paragraphs': len(content.split('\n\n')),
            'word_count': len(content.split()),
            'has_quotes': self._has_quotes(content),
            'has_citations': self._has_citations(content),
            'has_numbers': self._has_numbers(content),
            'has_dates': self._has_dates(content)
        }
        
        # Identify sections
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if line and line.isupper() or self._is_section_header(line):
                current_section = line
                analysis['sections'].append(current_section)
        
        return analysis
    
    def _has_title_page_info(self, content: str) -> bool:
        """Check if document has title page information"""
        title_indicators = ['title:', 'author:', 'course:', 'instructor:', 'date:']
        content_lower = content.lower()
        return any(indicator in content_lower for indicator in title_indicators)
    
    def _has_abstract(self, content: str) -> bool:
        """Check if document has an abstract"""
        abstract_patterns = [r'\babstract\b', r'\bsummary\b']
        content_lower = content.lower()
        return any(re.search(pattern, content_lower) for pattern in abstract_patterns)
    
    def _has_introduction(self, content: str) -> bool:
        """Check if document has an introduction"""
        intro_patterns = [r'\bintroduction\b', r'\bintro\b']
        content_lower = content.lower()
        return any(re.search(pattern, content_lower) for pattern in intro_patterns)
    
    def _has_conclusion(self, content: str) -> bool:
        """Check if document has a conclusion"""
        conclusion_patterns = [r'\bconclusion\b', r'\bconcluding\b']
        content_lower = content.lower()
        return any(re.search(pattern, content_lower) for pattern in conclusion_patterns)
    
    def _has_works_cited(self, content: str) -> bool:
        """Check if document has works cited page"""
        works_cited_patterns = [r'\bworks cited\b', r'\bbibliography\b']
        content_lower = content.lower()
        return any(re.search(pattern, content_lower) for pattern in works_cited_patterns)
    
    def _has_references(self, content: str) -> bool:
        """Check if document has references page"""
        references_patterns = [r'\breferences\b', r'\breference list\b']
        content_lower = content.lower()
        return any(re.search(pattern, content_lower) for pattern in references_patterns)
    
    def _has_running_head(self, content: str) -> bool:
        """Check if document has running head"""
        return 'running head' in content.lower()
    
    def _has_footnotes(self, content: str) -> bool:
        """Check if document has footnotes"""
        footnote_patterns = [r'\d+\.\s', r'\[\d+\]']
        return any(re.search(pattern, content) for pattern in footnote_patterns)
    
    def _has_bibliography(self, content: str) -> bool:
        """Check if document has bibliography"""
        return 'bibliography' in content.lower()
    
    def _has_numbered_references(self, content: str) -> bool:
        """Check if document has numbered references"""
        numbered_ref_pattern = r'\[\d+\]'
        return bool(re.search(numbered_ref_pattern, content))
    
    def _has_proper_quotes(self, content: str) -> bool:
        """Check if document has properly formatted quotes"""
        quote_patterns = [r'"[^"]*"', r"'[^']*'"]
        return any(re.search(pattern, content) for pattern in quote_patterns)
    
    def _has_page_numbers(self, content: str) -> bool:
        """Check if document has page numbers"""
        page_patterns = [r'page \d+', r'p\. \d+', r'pp\. \d+']
        return any(re.search(pattern, content.lower()) for pattern in page_patterns)
    
    def _has_quotes(self, content: str) -> bool:
        """Check if document contains quotes"""
        return '"' in content or "'" in content
    
    def _has_citations(self, content: str) -> bool:
        """Check if document contains citations"""
        citation_patterns = [r'\([^)]*\)', r'\[[^\]]*\]']
        return any(re.search(pattern, content) for pattern in citation_patterns)
    
    def _has_numbers(self, content: str) -> bool:
        """Check if document contains numbers"""
        return bool(re.search(r'\d+', content))
    
    def _has_dates(self, content: str) -> bool:
        """Check if document contains dates"""
        date_patterns = [r'\d{4}', r'\d{1,2}/\d{1,2}/\d{4}']
        return any(re.search(pattern, content) for pattern in date_patterns)
    
    def _is_section_header(self, line: str) -> bool:
        """Check if a line is a section header"""
        if not line:
            return False
        
        # Check if line is all caps or has common header patterns
        header_patterns = [
            r'^[A-Z\s]+$',  # All caps
            r'^\d+\.\s+[A-Z]',  # Numbered sections
            r'^[A-Z][a-z]+(\s+[A-Z][a-z]+)*$'  # Title case
        ]
        
        return any(re.match(pattern, line) for pattern in header_patterns)
    
    def get_document_statistics(self, content: str) -> Dict[str, Any]:
        """
        Get comprehensive statistics about the document
        """
        words = content.split()
        sentences = re.split(r'[.!?]+', content)
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'character_count': len(content),
            'average_words_per_sentence': len(words) / max(len(sentences), 1),
            'average_sentences_per_paragraph': len(sentences) / max(len(paragraphs), 1)
        }
