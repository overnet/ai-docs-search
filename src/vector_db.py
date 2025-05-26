import sqlite3
import os
import json
import numpy as np
from config import Config

class VectorDB:
    def __init__(
        self,
        db_path=Config.DB_FILE,
        embedding_dim=384,
    ):
        self.db_path = db_path
        self.embedding_dim = embedding_dim
        self.conn = None
        self.cursor = None
        self._connect_db()
        self._create_table()

    def _connect_db(self):
        """Establishes connection to SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            
            print(
                "Using optimized Python-based similarity search for vector operations."
            )
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            self.conn = None
            self.cursor = None

    def _create_table(self):
        """Creates the sentences table with vector support."""
        if not self.conn:
            print("Cannot create table: Database connection not established.")
            return

        # Use simple table structure for optimized Python-based search
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS sentences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL,
            sentence_text TEXT NOT NULL,
            embedding BLOB NOT NULL
        );
        """
        try:
            self.cursor.execute(create_table_sql)
            self.conn.commit()
            print("Table 'sentences' checked/created.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def insert_sentence_embedding(self, file_path, sentence_text, embedding):
        """Inserts a single sentence and its embedding into the database."""
        if not self.conn:
            print("Cannot insert: Database connection not established.")
            return

        try:
            # Simple insert for optimized Python-based search
            self.cursor.execute(
                "INSERT INTO sentences (file_path, sentence_text, embedding) VALUES (?, ?, ?)",
                (file_path, sentence_text, json.dumps(embedding)),
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")
            print(
                f"Problematic data: Path='{file_path}', Sentence='{sentence_text[:50]}'"
            )
            return None

    def clear_database(self):
        """Clears all data from the sentences table."""
        if not self.conn:
            print("Cannot clear: Database connection not established.")
            return
        try:
            self.cursor.execute("DELETE FROM sentences")
            self.conn.commit()
            print("Database cleared.")
        except sqlite3.Error as e:
            print(f"Error clearing database: {e}")

    def search_similar_sentences(
        self, 
        query_embedding, 
        limit=Config.DEFAULT_SEARCH_LIMIT, 
        distance_threshold=Config.DISTANCE_THRESHOLD
    ):
        """
        Searches for sentences most similar to the query embedding using Python-based similarity calculation.
        Only returns results with distance less than distance_threshold.
        """
        if not self.conn:
            print("Cannot search: Database connection not established.")
            return []

        print("Performing optimized Python-based similarity search.")
        results = self._fallback_python_search(query_embedding, limit, distance_threshold)

        # Ensure results are unique by file_path for final output
        unique_file_paths = []
        final_results = []
        for row in results:
            file_path, sentence_text, distance = row
            # Distance filtering already done in search methods, just check for uniqueness
            if file_path not in unique_file_paths:
                unique_file_paths.append(file_path)
                final_results.append({
                    "file_path": file_path,
                    "sentence": sentence_text,
                    "distance": distance
                })
        return final_results

    def _fallback_python_search(self, query_embedding, limit, distance_threshold):
        """
        Python-based search using numpy for similarity calculation.
        Provides accurate results for document collections.
        """
        all_sentences = self.cursor.execute(
            "SELECT file_path, sentence_text, embedding FROM sentences"
        ).fetchall()

        query_vec = np.array(query_embedding)
        # Normalize query vector for better cosine similarity calculation
        query_vec = query_vec / np.linalg.norm(query_vec)

        all_similarities = []
        for file_path, sentence_text, stored_embedding_blob in all_sentences:
            try:
                # For BLOB, load as JSON, then convert to numpy
                stored_vec = np.array(json.loads(stored_embedding_blob))
                # Normalize stored vector for better cosine similarity calculation
                stored_vec = stored_vec / np.linalg.norm(stored_vec)

                # Cosine similarity with normalized vectors
                similarity = np.dot(query_vec, stored_vec)
                distance = 1 - similarity
                
                # Store all distances for debugging
                all_similarities.append((distance, file_path, sentence_text))
            except json.JSONDecodeError:
                print(
                    f"Warning: Could not decode embedding for {file_path} - {sentence_text[:30]}. Skipping."
                )
                continue
            except Exception as e:
                print(
                    f"Error calculating similarity for {file_path} - {sentence_text[:30]}: {e}. Skipping."
                )
                continue

        # Sort by distance (ascending) - best matches first
        all_similarities.sort(key=lambda x: x[0])
        
        # Filter by threshold and return
        filtered_similarities = [(dist, fp, sent) for dist, fp, sent in all_similarities if dist < distance_threshold]
        return [(fp, sent, dist) for dist, fp, sent in filtered_similarities[:limit]]

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")


# Example usage (for testing this module independently)
if __name__ == "__main__":
    DB_FILE = "test_local_vector_db.db"

    db = VectorDB(
        db_path=DB_FILE, embedding_dim=384
    )

    # Clear previous data for testing
    db.clear_database()

    # Insert some dummy data
    sample_embedding_1 = [0.1] * 384  # Dummy
    sample_embedding_2 = [0.9] * 384  # Dummy, closer to query
    sample_embedding_query = [1.0] * 384  # Dummy query

    db.insert_sentence_embedding(
        "path/to/docA.txt",
        "This sentence talks about animals like dogs.",
        sample_embedding_1,
    )
    db.insert_sentence_embedding(
        "path/to/docB.txt", "The quick brown fox is a wild animal.", sample_embedding_2
    )

    # Search
    print("\n--- Search Results ---")
    results = db.search_similar_sentences(sample_embedding_query, limit=5)
    for res in results:
        print(
            f"File: {res['file_path']}, Sentence: {res['sentence'][:50]}..., Distance: {res['distance']:.4f}"
        )

    db.close()
