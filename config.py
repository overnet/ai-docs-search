import os

class Config:
    """Application configuration."""
    
    # Database settings
    DB_DIRECTORY = os.path.join("data", "db")
    DB_FILE = os.path.join(DB_DIRECTORY, "document_embeddings.db")
    
    # Docker environment settings
    HOST_ROOT = os.getenv("HOST_ROOT", "/host")
    VSS_EXTENSION_PATH = os.getenv("VSS_EXTENSION_PATH")
    
    # Search settings
    DISTANCE_THRESHOLD = 0.8  # Maximum distance for semantic similarity
    DEFAULT_SEARCH_LIMIT = 5  # Default number of results to return
    
    # Document processing settings
    MIN_SENTENCE_LENGTH = 10  # Minimum length of sentences to process
    SUPPORTED_EXTENSIONS = [".txt", ".csv", ".xml", ".pdf"]
    
    # Model settings
    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    
    @classmethod
    def ensure_directories(cls):
        """Ensure required directories exist."""
        os.makedirs(cls.DB_DIRECTORY, exist_ok=True) 