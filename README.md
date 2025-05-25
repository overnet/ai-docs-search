# AI Document Search

An AI-powered document search application that uses semantic search to find relevant content across multiple file types.

## Supported File Types

- Text files (.txt)
- CSV files (.csv)
- XML files (.xml)
- PDF files (.pdf)

## Installation

There are two ways to install the application:

### 1. Using pip with requirements.txt

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-docs-search.git
cd ai-docs-search

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Using setup.py

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-docs-search.git
cd ai-docs-search

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install the package
pip install -e .
```

## Optional: SQLite VSS Extension

For faster vector search capabilities, you can install the sqlite-vss extension:

1. Download the appropriate binary for your OS from [sqlite-vss releases](https://github.com/asg017/sqlite-vss/releases)
2. Place the binary in a known location
3. Update the `VSS_EXTENSION_PATH` in `app.py` to point to your binary

## Usage

1. Place your documents in a folder (e.g., "docs")
2. Run the application:
```bash
python app.py
```
3. Enter the path to your documents folder when prompted
4. Enter your search queries
5. Type 'q' to quit

## Example Queries

- "Tell me about planets in the solar system"
- "Show me information about customer orders"
- "Find documents about space exploration"

## Notes

- The application uses the NLTK library for text processing. Required NLTK data will be downloaded automatically on first run.
- The semantic search is powered by the sentence-transformers library using the all-MiniLM-L6-v2 model.
- For large document collections, installing the sqlite-vss extension is recommended for better performance. 