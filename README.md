# AI Document Formatting Agent

An intelligent AI agent that converts plain documents into various academic formats including MLA, APA, Chicago, and more.

## Features

- **Multi-format Support**: Convert documents to MLA, APA, Chicago, Harvard, and IEEE formats
- **Automatic Citation Management**: Generate and format citations, works cited pages, and bibliographies
- **Smart Content Analysis**: Identify missing information and suggest improvements
- **Page Numbering**: Automatic page numbering and formatting
- **Title Page Generation**: Create properly formatted title pages
- **Quote Formatting**: Properly format and cite quotations
- **Missing Information Detection**: Identify areas where additional information is needed

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key in a `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the application:
```bash
streamlit run app.py
```

## Supported Formats

- **MLA (Modern Language Association)**: Humanities and liberal arts
- **APA (American Psychological Association)**: Psychology, education, and sciences
- **Chicago**: History, literature, and arts
- **Harvard**: Business and social sciences
- **IEEE**: Engineering and technology

## File Support

- Plain text documents
- Word documents (.docx)
- PDF files
- Rich text format (.rtf)

## How It Works

1. **Document Analysis**: The AI analyzes your document structure and content
2. **Format Selection**: Choose your target academic format
3. **Content Processing**: The agent reformats content according to style guidelines
4. **Citation Generation**: Automatically generates proper citations and works cited
5. **Quality Check**: Identifies missing information and suggests improvements
6. **Output Generation**: Produces a properly formatted document

## Project Structure

```
AIAgent/
├── app.py                 # Main Streamlit application
├── document_processor.py  # Core document processing logic
├── format_converters/     # Format-specific conversion modules
├── citation_manager.py    # Citation and bibliography management
├── utils/                 # Utility functions
├── templates/             # Document templates
└── requirements.txt       # Python dependencies
```

