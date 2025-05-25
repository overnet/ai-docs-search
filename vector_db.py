import sqlite3
import os
import json  # For handling BLOB data if not using sqlite-vss correctly, but better to rely on sqlite-vss VECTOR type
import numpy as np  # For converting list to numpy array if needed for sqlite-vss


class VectorDB:
    def __init__(
        self,
        db_path="local_vector_db.db",
        embedding_dim=384,
        sqlite_vss_extension_path=None,
    ):
        self.db_path = db_path
        self.embedding_dim = embedding_dim
        self.sqlite_vss_extension_path = sqlite_vss_extension_path
        self.conn = None
        self.cursor = None
        self._connect_db()
        self._create_table()

    def _connect_db(self):
        """Establishes connection to SQLite database and loads sqlite-vss extension."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            if self.sqlite_vss_extension_path and os.path.exists(
                self.sqlite_vss_extension_path
            ):
                # Ensure the path is absolute and correct for your OS
                print(
                    f"Loading sqlite-vss extension from: {self.sqlite_vss_extension_path}"
                )
                self.conn.load_extension(self.sqlite_vss_extension_path)
                print("sqlite-vss extension loaded successfully.")
            else:
                print(
                    "Warning: sqlite-vss extension path not provided or not found. "
                    "Vector search functionality will be limited to Python-based similarity if implemented."
                )
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            if "not authorized to load extension" in str(e):
                print(
                    "Hint: On some systems, you might need to adjust permissions or run Python with specific flags (-E)."
                )
                print(
                    "Alternatively, ensure the extension file is in a trusted location or you're running from a virtual environment."
                )
            self.conn = None  # Set conn to None if connection fails
            self.cursor = None

    def _create_table(self):
        """Creates the sentences table with vector support."""
        if not self.conn:
            print("Cannot create table: Database connection not established.")
            return

        # Check if sqlite-vss is loaded to use VECTOR type
        is_vss_loaded = False
        try:
            self.cursor.execute(
                "SELECT vss_version()"
            )  # Check if vss functions are available
            is_vss_loaded = True
        except sqlite3.OperationalError:
            print("sqlite-vss extension not loaded. Using BLOB for embeddings.")

        if is_vss_loaded:
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS sentences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                sentence_text TEXT NOT NULL,
                embedding VECTOR({self.embedding_dim}) NOT NULL
            );
            """
        else:
            # Fallback if sqlite-vss isn't loaded (less efficient search)
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
            # If sqlite-vss is loaded, it handles list-to-VECTOR conversion
            # If not, convert list to JSON string for BLOB storage
            if hasattr(self.conn, "load_extension"):  # Heuristic for vss loaded
                try:
                    self.cursor.execute("SELECT vss_version()")  # Check again
                    embedding_to_store = embedding  # sqlite-vss handles list directly
                except sqlite3.OperationalError:
                    embedding_to_store = json.dumps(embedding)  # For BLOB
            else:
                embedding_to_store = json.dumps(embedding)  # For BLOB fallback

            self.cursor.execute(
                "INSERT INTO sentences (file_path, sentence_text, embedding) VALUES (?, ?, ?)",
                (file_path, sentence_text, embedding_to_store),
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

    def search_similar_sentences(self, query_embedding, limit=10, distance_threshold=0.5):
        """
        Searches for sentences most similar to the query embedding.
        Uses sqlite-vss if loaded, otherwise falls back to basic Python logic (less efficient).
        Only returns results with distance less than distance_threshold.
        """
        if not self.conn:
            print("Cannot search: Database connection not established.")
            return []

        results = []
        is_vss_loaded = False
        try:
            self.cursor.execute("SELECT vss_version()")
            is_vss_loaded = True
        except sqlite3.OperationalError:
            pass  # vss not loaded

        if is_vss_loaded:
            # Use sqlite-vss for efficient search
            try:
                query_sql = f"""
                SELECT
                    file_path,
                    sentence_text,
                    vss_search(embedding, ?) AS distance
                FROM
                    sentences
                WHERE
                    distance IS NOT NULL AND
                    distance < ?
                ORDER BY
                    distance
                LIMIT ?;
                """
                self.cursor.execute(query_sql, (query_embedding, distance_threshold, limit))
                results = self.cursor.fetchall()
                print(f"Search performed using sqlite-vss.")
            except sqlite3.Error as e:
                print(f"Error during sqlite-vss search: {e}")
                print("Falling back to Python-based search (less efficient).")
                results = self._fallback_python_search(query_embedding, limit, distance_threshold)
        else:
            print("Performing Python-based similarity search (sqlite-vss not loaded).")
            results = self._fallback_python_search(query_embedding, limit, distance_threshold)

        # Ensure results are unique by file_path for final output
        unique_file_paths = []
        final_results = []
        for row in results:
            file_path, sentence_text, distance = row
            if file_path not in unique_file_paths and distance < distance_threshold:
                unique_file_paths.append(file_path)
                final_results.append({
                    "file_path": file_path,
                    "sentence": sentence_text,
                    "distance": distance
                })
        return final_results

    def _fallback_python_search(self, query_embedding, limit, distance_threshold=0.5):
        """
        Fallback search using Python's numpy for similarity calculation.
        This is much slower for large datasets.
        """
        all_sentences = self.cursor.execute(
            "SELECT file_path, sentence_text, embedding FROM sentences"
        ).fetchall()

        query_vec = np.array(query_embedding)

        similarities = []
        for file_path, sentence_text, stored_embedding_blob in all_sentences:
            try:
                # For BLOB, load as JSON, then convert to numpy
                stored_vec = np.array(json.loads(stored_embedding_blob))

                # Cosine similarity (can be adapted for Euclidean if preferred)
                # Ensure vectors are normalized if using dot product for cosine similarity
                similarity = np.dot(query_vec, stored_vec) / (
                    np.linalg.norm(query_vec) * np.linalg.norm(stored_vec)
                )
                distance = 1 - similarity
                if distance < distance_threshold:
                    similarities.append((distance, file_path, sentence_text))
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

        # Sort by distance (ascending)
        similarities.sort(key=lambda x: x[0])
        return [(fp, sent, dist) for dist, fp, sent in similarities[:limit]]

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")


# Example usage (for testing this module independently)
if __name__ == "__main__":
    DB_FILE = "test_local_vector_db.db"
    # IMPORTANT: Replace with the actual path to your sqlite-vss extension file
    # For example: '/path/to/your/sqlite_vss.so' or 'C:\\path\\to\\sqlite_vss.dll'
    VSS_EXTENSION_PATH = (
        "/usr/local/lib/sqlite_vss0.so"  # Adjust for your OS and actual path
    )

    db = VectorDB(
        db_path=DB_FILE, embedding_dim=384, sqlite_vss_extension_path=VSS_EXTENSION_PATH
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
    os.remove(DB_FILE)  # Clean up test db
