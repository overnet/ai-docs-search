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
- **Vector Similarity Search**: Uses Python-based similarity calculation for accurate results
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
- **NumPy**: For efficient vector similarity calculations
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
   
   When prompted for a folder path, you can use `test_docs` to try the included sample files or use path to your local dir with files.

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
   
   When prompted for a folder path, you can use `test_docs` to try the included sample files or use path to your local dir with files.

## Usage Examples

### Starting the Application

1. **Using Docker (Recommended):**
   ```bash
   docker compose -f docker/docker-compose.yml run -i ai-docs-search
   ```

2. **Manual Installation:**
   ```bash
   export PYTHONPATH=src:$PYTHONPATH
   python src/app.py
   ```

### Sample Session

Here's a complete example of using the application:

```
--- AI Document Search Application ---

Loading embedding model 'sentence-transformers/all-MiniLM-L6-v2'...
Model loaded. Embedding dimension: 384
Using optimized Python-based similarity search for vector operations.

Enter the folder path to scan for files.
Folder path: test_docs

Scanning folder: /app/test_docs

--- Initializing Database ---
Processing CSV file: /app/test_docs/space_objects.csv
Processing TXT file: /app/test_docs/cats.txt
Processing PDF file: /app/test_docs/test_document.pdf
Processing TXT file: /app/test_docs/dogs.txt
Processing TXT file: /app/test_docs/space.txt
Processing XML file: /app/test_docs/sample_customer_orders.xml

Processing 112 sentences...
Vectorizing sentences: 100%|████████████| 112/112 [00:02<00:00, 37.70sent/s]

Database initialization complete.
```

### Search Query Examples

**Example 1: Finding Animal-Related Content**
```
Enter your search query: give me files with animals
Searching for content related to: 'give me files with animals'

--- Top Relevant Files ---
- /app/test_docs/cats.txt
- /app/test_docs/dogs.txt

--- Top Matching Sentences ---
  [File: dogs.txt] Sentence: 'Dogs are loyal pets....' (Distance: 0.6765)
  [File: cats.txt] Sentence: 'Cats are independent animals....' (Distance: 0.6986)
```

**Example 2: Finding Space-Related Content**
```
Enter your search query: give me files with space objects
Searching for content related to: 'give me files with space objects'

--- Top Relevant Files ---
- /app/test_docs/space.txt

--- Top Matching Sentences ---
  [File: space.txt] Sentence: 'He collected space memorabilia....' (Distance: 0.5963)
```

**Example 3: No Results Found**
```
Enter your search query: give me files with products
Searching for content related to: 'give me files with products'
No relevant files found.
```

### Understanding the Results

- **Distance Scores**: Lower values indicate better matches (0.0 = perfect match, 1.0 = no similarity)
- **Semantic Understanding**: The system finds relevant content even when exact keywords don't match
- **File Types**: Supports TXT, CSV, XML, and PDF files
- **Multiple Results**: Shows all relevant files and the best matching sentences from each

### Tips for Better Search Results

- Use descriptive phrases: "files about animals" works better than just "animals"
- Try different phrasings if you don't get expected results
- The system understands context and synonyms
- Distance scores below 0.7 typically indicate good semantic matches

### Test Data

The repository includes sample test files in the `test_docs/` directory:

- **cats.txt** - Information about cats and their behavior
- **dogs.txt** - Content about dogs as pets
- **space.txt** - Space-related content and astronomy
- **space_objects.csv** - Structured data about celestial objects
- **test_document.pdf** - Sample PDF document
- **sample_customer_orders.xml** - XML data with customer information

These files are perfect for testing the semantic search capabilities with queries like:
- "give me files with animals" → finds cats.txt and dogs.txt
- "give me files with space objects" → finds space.txt and space_objects.csv
- "show me customer data" → finds sample_customer_orders.xml

## Performance Notes

- The application uses Python-based similarity calculation with NumPy for accurate vector search
- Processing speed depends on:
  - Number and size of documents
  - Available system resources
  - System memory for vector calculations

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