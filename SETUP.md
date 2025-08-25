# Setup Guide for AI Document Formatting Agent

## Prerequisites

- Python 3.8 or higher
- OpenAI API key (get one at https://platform.openai.com/api-keys)

## Installation Steps

### 1. Clone the Repository
```bash
git clone <repository-url>
cd AIAgent
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
1. Copy the example environment file:
   ```bash
   cp env_example.txt .env
   ```

2. Edit the `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

### 4. Test the Installation
Run the test script to verify everything is working:
```bash
python test_agent.py
```

## Running the Application

### Web Interface (Recommended)
```bash
streamlit run app.py
```
This will open a web interface at `http://localhost:8501`

### Command Line Testing
```bash
python test_agent.py
```

## Features Overview

### Supported Formats
- **MLA**: Modern Language Association (Humanities)
- **APA**: American Psychological Association (Psychology, Sciences)
- **Chicago**: Chicago Manual of Style (History, Literature)
- **Harvard**: Harvard Referencing (Business, Social Sciences)
- **IEEE**: Institute of Electrical and Electronics Engineers (Engineering, Technology)

### Document Processing
- ✅ Title page generation
- ✅ Page numbering
- ✅ Proper margins and spacing
- ✅ Citation formatting
- ✅ Works cited/references pages
- ✅ Quote formatting
- ✅ Missing information detection

### File Support
- Plain text (.txt)
- Word documents (.docx)
- PDF files (.pdf) - Basic support
- Rich text format (.rtf)

## Usage Examples

### Web Interface
1. Open the web interface
2. Select your target format (MLA, APA, etc.)
3. Upload a document or paste text
4. Fill in document metadata (author, course, etc.)
5. Click "Format Document"
6. Download the formatted document

### Programmatic Usage
```python
from document_processor import DocumentProcessor

# Initialize the processor
processor = DocumentProcessor()

# Format a document
formatted_doc = processor.format_document(
    content="Your document text here...",
    format_type="mla",
    metadata={
        'author': 'John Doe',
        'title': 'My Research Paper',
        'course': 'English 101',
        'instructor': 'Dr. Smith',
        'due_date': '2024-01-15'
    }
)

print(formatted_doc)
```

## Troubleshooting

### Common Issues

1. **"OpenAI API key not found"**
   - Make sure you've created a `.env` file
   - Verify your API key is correct
   - Check that the `.env` file is in the project root

2. **Import errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

3. **File upload issues**
   - Supported formats: .txt, .docx, .pdf, .rtf
   - For PDF files, ensure PyPDF2 is installed

4. **Formatting errors**
   - Check that your document has proper structure
   - Ensure citations are in a recognizable format
   - Verify metadata is provided

### Getting Help

1. Run the test script: `python test_agent.py`
2. Check the console output for error messages
3. Verify your OpenAI API key has sufficient credits
4. Ensure your document content is properly formatted

## Advanced Configuration

### Custom Format Rules
You can modify format rules in the respective converter files:
- `format_converters/mla_converter.py`
- `format_converters/apa_converter.py`
- etc.

### Adding New Formats
1. Create a new converter class in `format_converters/`
2. Inherit from `BaseConverter`
3. Implement the required methods
4. Add the converter to `document_processor.py`

## API Usage

The agent uses OpenAI's API for advanced text processing. Make sure you have:
- A valid OpenAI API key
- Sufficient API credits
- Stable internet connection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. See the LICENSE file for details.
