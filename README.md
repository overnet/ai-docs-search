# AI Document Semantic Search

A powerful, local semantic search engine that helps you find relevant content across your documents using natural language queries. The application uses advanced AI to understand the meaning of your documents and queries, going beyond simple keyword matching.

## Project Structure

```
ai-docs-search/
├── src/                    # Python source code
│   ├── __init__.py
│   ├── app.py             # Main application entry point
│   ├── config.py          # Configuration settings
│   ├── document_parser.py # Document processing and text extraction
│   ├── embedding_model.py # Text vectorization using transformers
│   └── vector_db.py       # Database management and vector search
├── docker/                 # Docker-related files
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .dockerignore
├── docs/                   # Documentation
│   ├── project_zvit.txt   # Ukrainian project report
│   ├── project_zvit.pdf   # Ukrainian project report (PDF)
│   └── project_report.txt # English project report
├── tests/                  # Test files
├── test_docs/              # Sample test documents
├── data/                   # Database and data files
├── setup.py               # Package configuration
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── .gitignore             # Git ignore rules
```

## Features

- **Multiple File Format Support**: Process various file types:
  - Text files (.txt)
  - CSV files (.csv)
  - XML files (.xml)
  - PDF files (.pdf)

- **Semantic Search**: Find documents based on meaning, not just keywords
- **Vector Similarity Search**: Uses efficient SQLite VSS extension when available
- **Progress Tracking**: Visual progress bars for document processing
- **Docker Support**: Easy deployment using Docker

## How It Works

1. **Document Processing**:
   - Scans your specified folder for supported files
   - Extracts text content from each file
   - Breaks content into meaningful sentences
   - Generates embeddings using the all-MiniLM-L6-v2 model
   - Stores results in a SQLite database

2. **Search**:
   - Takes your natural language query
   - Converts it to the same embedding space
   - Finds semantically similar content
   - Returns relevant files and matching sentences

## Technologies Used

- **Python 3.8+**: Core programming language
- **sentence-transformers (all-MiniLM-L6-v2)**:
  - Pre-trained AI model for generating semantic embeddings
  - 384-dimensional vector space representation
  - Optimized for semantic similarity tasks
  - Efficient balance between performance and resource usage
  - Based on BERT architecture but 40% smaller
- **NLTK**: For text processing and sentence segmentation
- **SQLite**: For storing document embeddings
- **sqlite-vss**: For efficient vector similarity search
- **PyPDF2**: For PDF file processing
- **Docker**: For containerization and easy deployment

## AI Model Details

The application uses the all-MiniLM-L6-v2 model, which is a lightweight but powerful transformer model:

- **Architecture**: Based on BERT but optimized for sentence embeddings
- **Vector Size**: Produces 384-dimensional embeddings
- **Use Case**: Specifically trained for semantic similarity and search tasks
- **Performance**: 
  - Good balance between accuracy and speed
  - Can process thousands of sentences efficiently
  - Requires less memory than larger models like BERT-base
- **Features**:
  - Language Understanding: Captures semantic meaning beyond simple keywords
  - Cross-lingual Capabilities: Works with multiple languages
  - Context Awareness: Understands words based on their context
  - Efficient Inference: Optimized for production use

The model converts text into high-dimensional vectors where:
- Similar meanings are close together in vector space
- Different meanings are far apart
- Relationships between concepts are preserved

This allows the application to:
1. Find relevant content even when exact words don't match
2. Understand context and meaning, not just keywords
3. Handle variations in language and phrasing

## Installation

### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai-docs-search
   ```

2. Build and run using Docker Compose:
   ```bash
   # Build the Docker image
   docker compose -f docker/docker-compose.yml build

   # Run the application in interactive mode
   docker compose -f docker/docker-compose.yml run -i ai-docs-search
   ```

   Note: We use `run -i` instead of `up` to ensure proper handling of interactive input for the search queries.

### Manual Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai-docs-search
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package:
   ```bash
   pip install -e .
   ```

4. Run the application:
   ```bash
   # Set Python path to include src directory
   export PYTHONPATH=src:$PYTHONPATH
   python src/app.py
   ```

## Usage Examples

1. Start the application and enter the folder path you want to search through:
   ```
   Enter the folder path to scan for files.
   You can use:
   - Absolute path (e.g., /home/user/documents)
   - Relative path (e.g., test_docs or ./test_docs)
   ```

2. After processing, you can enter natural language queries. Examples:

   - Find animal-related content:
     ```
     Enter your search query: Tell me about animals
     ```
     The app will return files containing content semantically related to animals, even if they don't explicitly use the word "animals".

   - Find technical documentation:
     ```
     Enter your search query: Show me implementation details or technical specifications
     ```

   - Find content about specific topics:
     ```
     Enter your search query: Find information about data processing
     ```

3. For each query, the app shows:
   - List of relevant files
   - Matching sentences with similarity scores
   - Type 'q' to quit

## Performance Notes

- The application uses sqlite-vss for efficient vector similarity search when available
- Falls back to Python-based similarity calculation if sqlite-vss is not available
- Processing speed depends on:
  - Number and size of documents
  - Available system resources
  - Whether sqlite-vss is available

## Development

The application consists of main components located in the `src/` directory:

1. `src/app.py`: Main application entry point and orchestration
2. `src/document_parser.py`: Document processing and text extraction
3. `src/embedding_model.py`: Text vectorization using transformers
4. `src/vector_db.py`: Database management and vector search
5. `src/config.py`: Configuration settings and constants

Docker configuration is located in the `docker/` directory:
- `docker/Dockerfile`: Container build instructions
- `docker/docker-compose.yml`: Service orchestration
- `docker/.dockerignore`: Files to exclude from Docker build context

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your license here] 