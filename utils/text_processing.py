import re
from typing import List, Dict, Any

def clean_text(text: str) -> str:
    """
    Clean and normalize text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters that might cause issues
    text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\{\}\"\']', '', text)
    
    return text.strip()

def extract_sentences(text: str) -> List[str]:
    """
    Extract sentences from text
    """
    # Split on sentence endings
    sentences = re.split(r'[.!?]+', text)
    
    # Clean and filter empty sentences
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return sentences

def extract_paragraphs(text: str) -> List[str]:
    """
    Extract paragraphs from text
    """
    # Split on double newlines
    paragraphs = text.split('\n\n')
    
    # Clean and filter empty paragraphs
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    
    return paragraphs

def count_words(text: str) -> int:
    """
    Count words in text
    """
    words = text.split()
    return len(words)

def count_characters(text: str) -> int:
    """
    Count characters in text (excluding whitespace)
    """
    return len(text.replace(' ', ''))

def estimate_reading_time(text: str, words_per_minute: int = 200) -> float:
    """
    Estimate reading time in minutes
    """
    word_count = count_words(text)
    return word_count / words_per_minute

def find_quotes(text: str) -> List[Dict[str, Any]]:
    """
    Find and extract quotes from text
    """
    quotes = []
    
    # Pattern for quoted text
    quote_patterns = [
        r'"([^"]*)"',  # Double quotes
        r"'([^']*)'",  # Single quotes
        r'"([^"]*)"',  # Curly double quotes
        r"'([^']*)'",  # Curly single quotes
    ]
    
    for pattern in quote_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            quote_text = match.group(1)
            if len(quote_text.strip()) > 0:
                quotes.append({
                    'text': quote_text,
                    'start': match.start(),
                    'end': match.end(),
                    'full_match': match.group(0)
                })
    
    return quotes

def find_numbers(text: str) -> List[Dict[str, Any]]:
    """
    Find numbers in text
    """
    numbers = []
    
    # Pattern for various number formats
    number_patterns = [
        r'\b\d+\b',  # Whole numbers
        r'\b\d+\.\d+\b',  # Decimal numbers
        r'\b\d{4}\b',  # Years
        r'\b\d{1,2}/\d{1,2}/\d{4}\b',  # Dates
    ]
    
    for pattern in number_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            numbers.append({
                'text': match.group(0),
                'start': match.start(),
                'end': match.end(),
                'type': 'number'
            })
    
    return numbers

def find_dates(text: str) -> List[Dict[str, Any]]:
    """
    Find dates in text
    """
    dates = []
    
    # Pattern for various date formats
    date_patterns = [
        r'\b\d{1,2}/\d{1,2}/\d{4}\b',  # MM/DD/YYYY
        r'\b\d{1,2}-\d{1,2}-\d{4}\b',  # MM-DD-YYYY
        r'\b\d{4}-\d{1,2}-\d{1,2}\b',  # YYYY-MM-DD
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',  # Month DD, YYYY
    ]
    
    for pattern in date_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            dates.append({
                'text': match.group(0),
                'start': match.start(),
                'end': match.end(),
                'type': 'date'
            })
    
    return dates

def analyze_text_structure(text: str) -> Dict[str, Any]:
    """
    Analyze the structure of text
    """
    sentences = extract_sentences(text)
    paragraphs = extract_paragraphs(text)
    
    analysis = {
        'word_count': count_words(text),
        'character_count': count_characters(text),
        'sentence_count': len(sentences),
        'paragraph_count': len(paragraphs),
        'average_words_per_sentence': count_words(text) / max(len(sentences), 1),
        'average_sentences_per_paragraph': len(sentences) / max(len(paragraphs), 1),
        'reading_time_minutes': estimate_reading_time(text),
        'quotes': find_quotes(text),
        'numbers': find_numbers(text),
        'dates': find_dates(text)
    }
    
    return analysis

def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text
    """
    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)
    
    # Replace multiple newlines with double newlines
    text = re.sub(r'\n+', '\n\n', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text

def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract keywords from text (simple implementation)
    """
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
        'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
    }
    
    # Convert to lowercase and split into words
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Remove stop words and short words
    words = [word for word in words if word not in stop_words and len(word) > 3]
    
    # Count word frequency
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency and return top keywords
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    keywords = [word for word, freq in sorted_words[:max_keywords]]
    
    return keywords
