from transformers import AutoTokenizer, AutoModel
import torch
from sentence_transformers import (
    SentenceTransformer,
)  # Often used for convenient sentence embeddings
from tqdm import tqdm


class EmbeddingModel:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initializes the embedding model.
        all-MiniLM-L6-v2 is a good balance of size, speed, and quality (384 dimensions).
        """
        self.model_name = model_name
        # Using SentenceTransformer for ease of use. It wraps Hugging Face models.
        print(f"\nLoading embedding model '{model_name}'...")
        self.model = SentenceTransformer(model_name)
        self.embedding_dimension = self.model.get_sentence_embedding_dimension()
        print(
            f"Model loaded. Embedding dimension: {self.embedding_dimension}"
        )

    def get_embedding_dimension(self):
        """Returns the dimension of the embeddings produced by this model."""
        return self.embedding_dimension

    def get_sentence_embedding(self, sentence):
        """Generates an embedding vector for a single sentence."""
        if not sentence:
            return None
        # SentenceTransformer handles tokenization and pooling automatically
        embedding = self.model.encode(sentence, convert_to_tensor=True)
        return embedding.tolist()  # Return as a list for SQLite storage

    def get_batch_embeddings(self, sentences):
        """Generates embeddings for a list of sentences in a batch."""
        if not sentences:
            return []
        # Show progress bar for embedding generation
        embeddings = self.model.encode(sentences, convert_to_tensor=True, show_progress_bar=True)
        return embeddings.tolist()  # Return as a list of lists


# Example usage (for testing this module independently)
if __name__ == "__main__":
    embedder = EmbeddingModel()
    test_sentence = "The cat sat on the mat."
    embedding = embedder.get_sentence_embedding(test_sentence)
    print(f"\nEmbedding for '{test_sentence}': {embedding[:5]}... (first 5 elements)")
    print(f"Embedding dimension: {len(embedding)}")

    batch_sentences = [
        "Dogs are loyal companions.",
        "A swift deer runs through the forest.",
        "The computer processed the data quickly.",
    ]
    batch_embeddings = embedder.get_batch_embeddings(batch_sentences)
    print(
        f"\nEmbeddings for batch (first 5 elements of first embedding):\n{batch_embeddings[0][:5]}..."
    )
