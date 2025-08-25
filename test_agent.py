#!/usr/bin/env python3
"""
Test script for the AI Document Formatting Agent
"""

import os
from dotenv import load_dotenv
from document_processor import DocumentProcessor
from citation_manager import CitationManager

# Load environment variables
load_dotenv()

def test_document_processing():
    """
    Test the document processing functionality
    """
    print("🧪 Testing AI Document Formatting Agent...")
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OpenAI API key not found. Please set OPENAI_API_KEY in your .env file")
        print("   Copy env_example.txt to .env and add your API key")
        return
    
    # Sample document content
    sample_content = """
    The Impact of Artificial Intelligence on Modern Education

    Artificial intelligence has revolutionized the way we approach education in the 21st century. 
    According to Smith (2023), AI-powered learning systems have shown a 40% improvement in student 
    engagement compared to traditional methods. "The integration of AI in classrooms represents a 
    paradigm shift in educational technology," states Johnson (2022, p. 45).

    Machine learning algorithms can now personalize learning experiences for individual students, 
    adapting to their unique learning styles and pace. This personalized approach has been shown 
    to improve retention rates significantly (Brown, 2021). However, some educators express concerns 
    about the potential loss of human interaction in the learning process.

    The future of education lies in finding the right balance between AI assistance and human 
    guidance. As noted by Davis (2023), "Technology should enhance, not replace, the teacher-student 
    relationship." This sentiment is echoed by many educational researchers who emphasize the 
    importance of maintaining human connections in learning environments.

    In conclusion, while AI offers tremendous potential for improving educational outcomes, it 
    must be implemented thoughtfully and with careful consideration of its impact on the human 
    aspects of learning.
    """
    
    # Sample metadata
    metadata = {
        'author': 'Jane Doe',
        'course': 'Education Technology 101',
        'instructor': 'Dr. Smith',
        'due_date': '2024-01-15',
        'title': 'The Impact of Artificial Intelligence on Modern Education'
    }
    
    # Initialize processors
    doc_processor = DocumentProcessor()
    citation_manager = CitationManager()
    
    print("📄 Processing sample document...")
    
    # Test different formats
    formats = ['mla', 'apa', 'chicago', 'harvard', 'ieee']
    
    for format_type in formats:
        print(f"\n🎯 Testing {format_type.upper()} format:")
        
        try:
            # Process the document
            formatted_doc = doc_processor.format_document(
                content=sample_content,
                format_type=format_type,
                metadata=metadata
            )
            
            # Analyze missing information
            missing_info = doc_processor.analyze_missing_information(sample_content, format_type)
            
            print(f"✅ {format_type.upper()} formatting completed successfully!")
            print(f"📊 Document statistics:")
            
            stats = doc_processor.get_document_statistics(sample_content)
            print(f"   - Words: {stats['word_count']}")
            print(f"   - Sentences: {stats['sentence_count']}")
            print(f"   - Paragraphs: {stats['paragraph_count']}")
            print(f"   - Reading time: {stats['reading_time_minutes']:.1f} minutes")
            
            if missing_info:
                print(f"⚠️  Missing information detected:")
                for item in missing_info:
                    print(f"   - {item}")
            else:
                print("✅ No missing information detected!")
            
            # Show a preview of the formatted document
            print(f"📖 Formatted document preview (first 200 characters):")
            preview = formatted_doc[:200] + "..." if len(formatted_doc) > 200 else formatted_doc
            print(f"   {preview}")
            
        except Exception as e:
            print(f"❌ Error processing {format_type.upper()} format: {str(e)}")
    
    print("\n🎉 Testing completed!")

def test_citation_extraction():
    """
    Test citation extraction functionality
    """
    print("\n🔍 Testing citation extraction...")
    
    sample_text = "According to Smith (2023), AI has revolutionized education. Johnson (2022, p. 45) states that 'technology enhances learning.'"
    
    citation_manager = CitationManager()
    citations = citation_manager.extract_citations(sample_text)
    
    print(f"Found {len(citations)} citations:")
    for i, citation in enumerate(citations, 1):
        print(f"  {i}. {citation}")

if __name__ == "__main__":
    test_document_processing()
    test_citation_extraction()
