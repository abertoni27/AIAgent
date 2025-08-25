import streamlit as st
import os
from dotenv import load_dotenv
from document_processor import DocumentProcessor
from citation_manager import CitationManager
import tempfile
import base64

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Document Formatting Agent",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .format-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">📚 AI Document Formatting Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform your plain documents into professionally formatted academic papers</p>', unsafe_allow_html=True)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        st.error("⚠️ OpenAI API key not found. Please add your API key to the .env file.")
        st.info("Create a .env file in the project root with: OPENAI_API_KEY=your_api_key_here")
        return
    
    # Sidebar for format selection
    with st.sidebar:
        st.header("🎯 Choose Your Format")
        
        format_options = {
            "MLA (Modern Language Association)": "mla",
            "APA (American Psychological Association)": "apa", 
            "Chicago": "chicago",
            "Harvard": "harvard",
            "IEEE": "ieee"
        }
        
        selected_format = st.selectbox(
            "Select Academic Format:",
            list(format_options.keys()),
            help="Choose the academic format you want to convert your document to"
        )
        
        st.markdown("---")
        st.header("📋 Format Features")
        
        format_features = {
            "mla": ["Double-spaced text", "1-inch margins", "Header with last name and page number", "Works Cited page"],
            "apa": ["Double-spaced text", "1-inch margins", "Running head", "References page"],
            "chicago": ["Double-spaced text", "1-inch margins", "Footnotes or endnotes", "Bibliography"],
            "harvard": ["Double-spaced text", "1-inch margins", "In-text citations", "Reference list"],
            "ieee": ["Single-spaced text", "1-inch margins", "Numbered references", "Reference list"]
        }
        
        selected_format_key = format_options[selected_format]
        for feature in format_features[selected_format_key]:
            st.markdown(f"✅ {feature}")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📄 Upload Your Document")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a document to format:",
            type=['txt', 'docx', 'pdf', 'rtf'],
            help="Supported formats: .txt, .docx, .pdf, .rtf"
        )
        
        # Text input as alternative
        st.markdown("---")
        st.subheader("Or paste your text directly:")
        text_input = st.text_area(
            "Enter your document text:",
            height=300,
            placeholder="Paste your document content here..."
        )
        
        # Document metadata
        st.markdown("---")
        st.subheader("📝 Document Information")
        
        col_meta1, col_meta2 = st.columns(2)
        with col_meta1:
            author_name = st.text_input("Author Name:", placeholder="Your full name")
            course_name = st.text_input("Course Name:", placeholder="e.g., English 101")
        
        with col_meta2:
            instructor_name = st.text_input("Instructor Name:", placeholder="Professor's name")
            due_date = st.date_input("Due Date:")
        
        document_title = st.text_input("Document Title:", placeholder="Your paper title")
        
        # Process button
        if st.button("🚀 Format Document", type="primary", use_container_width=True):
            if uploaded_file or text_input:
                process_document(uploaded_file, text_input, selected_format_key, {
                    'author': author_name,
                    'course': course_name,
                    'instructor': instructor_name,
                    'due_date': due_date,
                    'title': document_title
                })
            else:
                st.error("Please upload a file or enter text to format.")
    
    with col2:
        st.header("📊 Document Analysis")
        
        if uploaded_file or text_input:
            # Show document stats
            content = get_document_content(uploaded_file, text_input)
            if content:
                word_count = len(content.split())
                char_count = len(content)
                
                st.metric("Word Count", word_count)
                st.metric("Character Count", char_count)
                
                # Estimate reading time
                reading_time = word_count / 200  # Average reading speed
                st.metric("Estimated Reading Time", f"{reading_time:.1f} minutes")
                
                # Show format preview
                st.markdown("---")
                st.subheader("🎨 Format Preview")
                st.markdown(f"**Selected Format:** {selected_format}")
                
                # Show what will be added
                st.markdown("**Will be added:**")
                st.markdown("✅ Title page")
                st.markdown("✅ Page numbers")
                st.markdown("✅ Proper margins and spacing")
                st.markdown("✅ Citations and references")
                st.markdown("✅ Works cited/bibliography")

def get_document_content(uploaded_file, text_input):
    """Extract content from uploaded file or text input"""
    if uploaded_file:
        try:
            if uploaded_file.type == "text/plain":
                return uploaded_file.read().decode('utf-8')
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                from docx import Document
                doc = Document(uploaded_file)
                return "\n".join([paragraph.text for paragraph in doc.paragraphs])
            else:
                st.error("File type not supported yet. Please use .txt or .docx files.")
                return None
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            return None
    elif text_input:
        return text_input
    return None

def process_document(uploaded_file, text_input, format_type, metadata):
    """Process the document and format it according to the selected style"""
    
    with st.spinner("🤖 AI is analyzing and formatting your document..."):
        try:
            # Initialize processors
            doc_processor = DocumentProcessor()
            citation_manager = CitationManager()
            
            # Get document content
            content = get_document_content(uploaded_file, text_input)
            if not content:
                return
            
            # Process the document
            formatted_doc = doc_processor.format_document(
                content=content,
                format_type=format_type,
                metadata=metadata
            )
            
            # Analyze for missing information
            missing_info = doc_processor.analyze_missing_information(content, format_type)
            
            # Display results
            st.success("✅ Document formatted successfully!")
            
            # Show formatted document
            st.markdown("---")
            st.header("📄 Formatted Document")
            
            # Create tabs for different views
            tab1, tab2, tab3 = st.tabs(["📖 Formatted Text", "🔍 Missing Information", "📥 Download"])
            
            with tab1:
                st.text_area(
                    "Formatted Document:",
                    value=formatted_doc,
                    height=600,
                    disabled=True
                )
            
            with tab2:
                if missing_info:
                    st.warning("⚠️ The following information may be missing or incomplete:")
                    for item in missing_info:
                        st.markdown(f"• {item}")
                else:
                    st.success("✅ No missing information detected!")
            
            with tab3:
                # Create downloadable file
                create_download_link(formatted_doc, f"formatted_document_{format_type}.txt")
                
        except Exception as e:
            st.error(f"❌ Error processing document: {str(e)}")

def create_download_link(content, filename):
    """Create a download link for the formatted document"""
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 Download Formatted Document</a>'
    st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
