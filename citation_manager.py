import re
import openai
import os
from typing import Dict, List, Any, Tuple
from datetime import datetime

class CitationManager:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Citation patterns for different formats
        self.citation_patterns = {
            'mla': [
                r'\(([^)]+)\)',  # (Author Page)
                r'\[([^\]]+)\]',  # [Author Page]
            ],
            'apa': [
                r'\(([^)]+)\)',  # (Author, Year)
                r'\[([^\]]+)\]',  # [Author, Year]
            ],
            'chicago': [
                r'\(([^)]+)\)',  # (Author Year, Page)
                r'\[([^\]]+)\]',  # [Author Year, Page]
            ],
            'harvard': [
                r'\(([^)]+)\)',  # (Author, Year)
                r'\[([^\]]+)\]',  # [Author, Year]
            ],
            'ieee': [
                r'\[([^\]]+)\]',  # [1], [2], etc.
            ]
        }
    
    def extract_citations(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract citations from document content
        """
        citations = []
        
        # Look for various citation patterns
        patterns = [
            r'\(([^)]+)\)',  # Parenthetical citations
            r'\[([^\]]+)\]',  # Bracket citations
            r'([A-Z][a-z]+ [A-Z][a-z]+ \d{4})',  # Author Year patterns
            r'([A-Z][a-z]+, \d{4})',  # Author, Year patterns
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                citation_text = match.group(1) if match.groups() else match.group(0)
                
                # Analyze the citation
                citation_info = self._analyze_citation(citation_text)
                if citation_info:
                    citations.append({
                        'text': citation_text,
                        'type': citation_info['type'],
                        'author': citation_info.get('author'),
                        'year': citation_info.get('year'),
                        'page': citation_info.get('page'),
                        'title': citation_info.get('title'),
                        'source': citation_info.get('source'),
                        'position': match.start()
                    })
        
        return citations
    
    def _analyze_citation(self, citation_text: str) -> Dict[str, Any]:
        """
        Analyze a citation text to extract components
        """
        citation_text = citation_text.strip()
        
        # Try to identify citation type and extract components
        if re.match(r'^\d+$', citation_text):
            # IEEE style numbered reference
            return {
                'type': 'ieee',
                'number': int(citation_text)
            }
        
        # Look for author patterns
        author_patterns = [
            r'^([A-Z][a-z]+ [A-Z][a-z]+)',  # First Last
            r'^([A-Z][a-z]+, [A-Z][a-z]+)',  # Last, First
            r'^([A-Z][a-z]+)',  # Single name
        ]
        
        for pattern in author_patterns:
            author_match = re.match(pattern, citation_text)
            if author_match:
                author = author_match.group(1)
                remaining = citation_text[author_match.end():].strip()
                
                # Look for year
                year_match = re.search(r'(\d{4})', remaining)
                year = year_match.group(1) if year_match else None
                
                # Look for page
                page_match = re.search(r'(\d+)(?:\s*[pP]\.?\s*)?$', remaining)
                page = page_match.group(1) if page_match else None
                
                return {
                    'type': 'author_year',
                    'author': author,
                    'year': year,
                    'page': page
                }
        
        # Look for title patterns
        if '"' in citation_text or "'" in citation_text:
            # Quoted title
            title_match = re.search(r'["\']([^"\']+)["\']', citation_text)
            if title_match:
                return {
                    'type': 'title',
                    'title': title_match.group(1)
                }
        
        return None
    
    def generate_works_cited(self, citations: List[Dict[str, Any]], format_type: str) -> str:
        """
        Generate a works cited/references page based on the format
        """
        if not citations:
            return ""
        
        if format_type == 'mla':
            return self._generate_mla_works_cited(citations)
        elif format_type == 'apa':
            return self._generate_apa_references(citations)
        elif format_type == 'chicago':
            return self._generate_chicago_bibliography(citations)
        elif format_type == 'harvard':
            return self._generate_harvard_references(citations)
        elif format_type == 'ieee':
            return self._generate_ieee_references(citations)
        else:
            return self._generate_generic_references(citations)
    
    def _generate_mla_works_cited(self, citations: List[Dict[str, Any]]) -> str:
        """
        Generate MLA format works cited page
        """
        works_cited = "Works Cited\n\n"
        
        # Group citations by author
        author_citations = {}
        for citation in citations:
            author = citation.get('author', 'Unknown Author')
            if author not in author_citations:
                author_citations[author] = []
            author_citations[author].append(citation)
        
        # Generate entries
        for author, author_cits in author_citations.items():
            for i, citation in enumerate(author_cits):
                if i == 0:
                    # First citation for this author
                    works_cited += f"{author}. "
                else:
                    # Subsequent citations - use dashes
                    works_cited += "---. "
                
                # Add title if available
                if citation.get('title'):
                    works_cited += f'"{citation["title"]}." '
                
                # Add source if available
                if citation.get('source'):
                    works_cited += f"{citation['source']}, "
                
                # Add year if available
                if citation.get('year'):
                    works_cited += f"{citation['year']}, "
                
                # Add page if available
                if citation.get('page'):
                    works_cited += f"p. {citation['page']}.\n\n"
                else:
                    works_cited += ".\n\n"
        
        return works_cited
    
    def _generate_apa_references(self, citations: List[Dict[str, Any]]) -> str:
        """
        Generate APA format references page
        """
        references = "References\n\n"
        
        # Group citations by author
        author_citations = {}
        for citation in citations:
            author = citation.get('author', 'Unknown Author')
            if author not in author_citations:
                author_citations[author] = []
            author_citations[author].append(citation)
        
        # Generate entries
        for author, author_cits in author_citations.items():
            for citation in author_cits:
                # Author name
                references += f"{author}. "
                
                # Year
                if citation.get('year'):
                    references += f"({citation['year']}). "
                
                # Title
                if citation.get('title'):
                    references += f"{citation['title']}. "
                
                # Source
                if citation.get('source'):
                    references += f"{citation['source']}."
                
                # Page
                if citation.get('page'):
                    references += f" p. {citation['page']}."
                
                references += "\n\n"
        
        return references
    
    def _generate_chicago_bibliography(self, citations: List[Dict[str, Any]]) -> str:
        """
        Generate Chicago format bibliography
        """
        bibliography = "Bibliography\n\n"
        
        # Group citations by author
        author_citations = {}
        for citation in citations:
            author = citation.get('author', 'Unknown Author')
            if author not in author_citations:
                author_citations[author] = []
            author_citations[author].append(citation)
        
        # Generate entries
        for author, author_cits in author_citations.items():
            for citation in author_cits:
                bibliography += f"{author}. "
                
                # Title
                if citation.get('title'):
                    bibliography += f'"{citation["title"]}." '
                
                # Source
                if citation.get('source'):
                    bibliography += f"{citation['source']}, "
                
                # Year
                if citation.get('year'):
                    bibliography += f"{citation['year']}."
                
                # Page
                if citation.get('page'):
                    bibliography += f" {citation['page']}."
                
                bibliography += "\n\n"
        
        return bibliography
    
    def _generate_harvard_references(self, citations: List[Dict[str, Any]]) -> str:
        """
        Generate Harvard format reference list
        """
        references = "Reference List\n\n"
        
        # Group citations by author
        author_citations = {}
        for citation in citations:
            author = citation.get('author', 'Unknown Author')
            if author not in author_citations:
                author_citations[author] = []
            author_citations[author].append(citation)
        
        # Generate entries
        for author, author_cits in author_citations.items():
            for citation in author_cits:
                references += f"{author}. "
                
                # Year
                if citation.get('year'):
                    references += f"({citation['year']}). "
                
                # Title
                if citation.get('title'):
                    references += f"{citation['title']}. "
                
                # Source
                if citation.get('source'):
                    references += f"{citation['source']}."
                
                references += "\n\n"
        
        return references
    
    def _generate_ieee_references(self, citations: List[Dict[str, Any]]) -> str:
        """
        Generate IEEE format reference list
        """
        references = "References\n\n"
        
        # Number citations
        for i, citation in enumerate(citations, 1):
            references += f"[{i}] "
            
            # Author
            if citation.get('author'):
                references += f"{citation['author']}, "
            
            # Title
            if citation.get('title'):
                references += f'"{citation["title"]}," '
            
            # Source
            if citation.get('source'):
                references += f"{citation['source']}, "
            
            # Year
            if citation.get('year'):
                references += f"{citation['year']}."
            
            # Page
            if citation.get('page'):
                references += f" pp. {citation['page']}."
            
            references += "\n\n"
        
        return references
    
    def _generate_generic_references(self, citations: List[Dict[str, Any]]) -> str:
        """
        Generate a generic reference list
        """
        references = "References\n\n"
        
        for i, citation in enumerate(citations, 1):
            references += f"{i}. "
            
            if citation.get('author'):
                references += f"{citation['author']}, "
            
            if citation.get('title'):
                references += f'"{citation["title"]}," '
            
            if citation.get('source'):
                references += f"{citation['source']}, "
            
            if citation.get('year'):
                references += f"{citation['year']}."
            
            if citation.get('page'):
                references += f" p. {citation['page']}."
            
            references += "\n\n"
        
        return references
    
    def format_in_text_citation(self, citation: Dict[str, Any], format_type: str) -> str:
        """
        Format an in-text citation according to the specified format
        """
        if format_type == 'mla':
            return self._format_mla_citation(citation)
        elif format_type == 'apa':
            return self._format_apa_citation(citation)
        elif format_type == 'chicago':
            return self._format_chicago_citation(citation)
        elif format_type == 'harvard':
            return self._format_harvard_citation(citation)
        elif format_type == 'ieee':
            return self._format_ieee_citation(citation)
        else:
            return self._format_generic_citation(citation)
    
    def _format_mla_citation(self, citation: Dict[str, Any]) -> str:
        """Format MLA in-text citation"""
        parts = []
        
        if citation.get('author'):
            parts.append(citation['author'])
        
        if citation.get('page'):
            parts.append(citation['page'])
        
        return f"({' '.join(parts)})"
    
    def _format_apa_citation(self, citation: Dict[str, Any]) -> str:
        """Format APA in-text citation"""
        parts = []
        
        if citation.get('author'):
            parts.append(citation['author'])
        
        if citation.get('year'):
            parts.append(citation['year'])
        
        if citation.get('page'):
            parts.append(f"p. {citation['page']}")
        
        return f"({', '.join(parts)})"
    
    def _format_chicago_citation(self, citation: Dict[str, Any]) -> str:
        """Format Chicago in-text citation"""
        parts = []
        
        if citation.get('author'):
            parts.append(citation['author'])
        
        if citation.get('year'):
            parts.append(citation['year'])
        
        if citation.get('page'):
            parts.append(f"p. {citation['page']}")
        
        return f"({' '.join(parts)})"
    
    def _format_harvard_citation(self, citation: Dict[str, Any]) -> str:
        """Format Harvard in-text citation"""
        parts = []
        
        if citation.get('author'):
            parts.append(citation['author'])
        
        if citation.get('year'):
            parts.append(citation['year'])
        
        return f"({', '.join(parts)})"
    
    def _format_ieee_citation(self, citation: Dict[str, Any]) -> str:
        """Format IEEE in-text citation"""
        return f"[{citation.get('number', '?')}]"
    
    def _format_generic_citation(self, citation: Dict[str, Any]) -> str:
        """Format generic in-text citation"""
        parts = []
        
        if citation.get('author'):
            parts.append(citation['author'])
        
        if citation.get('year'):
            parts.append(citation['year'])
        
        return f"({', '.join(parts)})"
