import os
import sys
from document_parser import DocumentParser
from embedding_model import EmbeddingModel
from vector_db import VectorDB
from tqdm import tqdm

# --- Configuration ---
DB_FILE = "document_embeddings.db"
# IMPORTANT: Set this to the actual path of your sqlite-vss extension file
# Download from https://github.com/asg017/sqlite-vss/releases
# Example for Linux: VSS_EXTENSION_PATH = "/usr/local/lib/sqlite_vss0.so"
# Example for macOS: VSS_EXTENSION_PATH = "/usr/local/lib/sqlite_vss0.dylib"
# Example for Windows: VSS_EXTENSION_PATH = "C:\\path\\to\\sqlite_vss0.dll"
# If you don't provide a valid path, it will fall back to Python-based search (slower).
VSS_EXTENSION_PATH = None  # <--- !!! REPLACE WITH YOUR ACTUAL PATH !!!
# --- End Configuration ---


def initialize_database(db_manager, parser, embedder, folder_path):
    """
    Scans the specified folder, processes files, and populates the database.
    """
    print("\n--- Initializing Database ---")
    db_manager.clear_database()  # Clear existing data

    scanned_data = parser.scan_folder(folder_path)
    if not scanned_data:
        print("No .txt files found or processed in the folder.")
        return

    print(f"\nProcessing {len(scanned_data)} sentences...")

    # Process in batches for efficiency (optional, but good practice)
    batch_size = 32  # Adjust based on your system's memory and model
    progress_bar = tqdm(total=len(scanned_data), desc="Vectorizing sentences", unit="sent")
    
    for i in range(0, len(scanned_data), batch_size):
        batch = scanned_data[i : i + batch_size]
        sentences = [item[1] for item in batch]
        file_paths = [item[0] for item in batch]

        embeddings = embedder.get_batch_embeddings(sentences)

        for j in range(len(sentences)):
            db_manager.insert_sentence_embedding(
                file_paths[j], sentences[j], embeddings[j]
            )
        progress_bar.update(len(batch))
    
    progress_bar.close()
    print("\nDatabase initialization complete.")


def main():
    print("--- AI Document Search Application ---")

    # Initialize components
    parser = DocumentParser()
    embedder = EmbeddingModel()
    db_manager = VectorDB(
        db_path=DB_FILE,
        embedding_dim=embedder.get_embedding_dimension(),
        sqlite_vss_extension_path=VSS_EXTENSION_PATH,
    )

    # --- Step 1: Ingest Data ---
    folder_path = input("Enter the folder path to scan for .txt files: ")
    if not os.path.isdir(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        db_manager.close()
        sys.exit(1)

    initialize_database(db_manager, parser, embedder, folder_path)

    # --- Step 2: Perform Searches ---
    while True:
        query = input(
            "\nEnter your search query (e.g., 'animal description', or 'q' to quit): "
        )
        if query.lower() == "q":
            break

        print(f"Searching for content related to: '{query}'")
        query_embedding = embedder.get_sentence_embedding(query)
        if query_embedding is None:
            print("Could not generate embedding for the query. Please try again.")
            continue

        search_results = db_manager.search_similar_sentences(
            query_embedding, limit=5
        )  # Get top 5 sentences

        if not search_results:
            print("No relevant files found.")
        else:
            print("\n--- Top Relevant Files ---")
            # Collect unique file paths
            relevant_files = set()
            for res in search_results:
                relevant_files.add(res["file_path"])

            for f_path in relevant_files:
                print(f"- {f_path}")

            # Optionally, show the top matching sentences
            print("\n--- Top Matching Sentences ---")
            for res in search_results:
                print(
                    f"  [File: {os.path.basename(res['file_path'])}] Sentence: '{res['sentence'][:70]}...' (Distance: {res['distance']:.4f})"
                )

    db_manager.close()
    print("\nApplication closed. Goodbye!")


if __name__ == "__main__":
    main()
