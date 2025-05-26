# AI Document Semantic Search

A powerful, AI-driven semantic search engine that helps you find relevant content across your documents using natural language queries. The application leverages advanced AI models and machine learning to understand the meaning of your documents and queries, going far beyond simple keyword matching to deliver intelligent, context-aware search results.

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

- **AI-Powered Semantic Search**: Find documents based on meaning and context using advanced AI models, not just keywords
- **Machine Learning Vector Search**: Uses AI-generated embeddings and Python-based similarity calculation for intelligent results
- **Natural Language Understanding**: AI processes your queries to understand intent and context
- **Progress Tracking**: Visual progress bars for document processing
- **Docker Support**: Easy deployment using Docker

## How It Works

1. **AI-Powered Document Processing**:
   - Scans your specified folder for supported files
   - Extracts text content from each file
   - Breaks content into meaningful sentences using AI-powered text processing
   - Generates high-dimensional vector embeddings using the all-MiniLM-L6-v2 AI model
   - Stores AI-generated embeddings in a SQLite database

2. **Intelligent AI Search**:
   - Takes your natural language query
   - Uses AI to convert it to the same high-dimensional embedding space
   - Employs machine learning algorithms to find semantically similar content
   - Returns AI-ranked relevant files and matching sentences based on semantic similarity

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

This AI-powered approach allows the application to:
1. Find relevant content even when exact words don't match using machine learning
2. Understand context and meaning through AI, not just keywords
3. Handle variations in language and phrasing with intelligent natural language processing
4. Provide human-like understanding of document content and search intent

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

Loading AI embedding model 'sentence-transformers/all-MiniLM-L6-v2'...
AI Model loaded. Embedding dimension: 384
Using AI-optimized Python-based similarity search for vector operations.

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

### Understanding the AI Results

- **AI Distance Scores**: Lower values indicate better AI-calculated matches (0.0 = perfect match, 1.0 = no similarity)
- **AI Semantic Understanding**: The AI system finds relevant content even when exact keywords don't match
- **File Types**: AI processes TXT, CSV, XML, and PDF files intelligently
- **AI-Ranked Results**: Shows all relevant files and the best AI-matching sentences from each

### Tips for Better AI Search Results

- Use descriptive phrases: "files about animals" works better than just "animals" for AI understanding
- Try different phrasings if you don't get expected results - the AI learns from natural language
- The AI system understands context, synonyms, and related concepts
- AI distance scores below 0.7 typically indicate good semantic matches
- Write queries as you would ask a human - the AI understands natural language

### Test Data

The repository includes sample test files in the `test_docs/` directory:

- **cats.txt** - Information about cats and their behavior
- **dogs.txt** - Content about dogs as pets
- **space.txt** - Space-related content and astronomy
- **space_objects.csv** - Structured data about celestial objects
- **test_document.pdf** - Sample PDF document
- **sample_customer_orders.xml** - XML data with customer information

These files are perfect for testing the AI semantic search capabilities with natural language queries like:
- "give me files with animals" → AI finds cats.txt and dogs.txt
- "give me files with space objects" → AI finds space.txt and space_objects.csv
- "show me customer data" → AI finds sample_customer_orders.xml

## AI Performance Notes

- The application uses AI-powered Python-based similarity calculation with NumPy for accurate vector search
- AI processing speed depends on:
  - Number and size of documents
  - Available system resources for AI computations
  - System memory for AI vector calculations and model operations

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