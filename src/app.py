import os
import sys
from document_parser import DocumentParser
from embedding_model import EmbeddingModel
from vector_db import VectorDB
from tqdm import tqdm
from config import Config

def convert_host_path_to_container(host_path):
    """Convert a host path to its equivalent in the container."""
    # If it's a relative path, make it absolute relative to current directory
    if not os.path.isabs(host_path):
        host_path = os.path.abspath(host_path)
    
    # If it's already an absolute path in the container, return as is
    if host_path.startswith(Config.HOST_ROOT):
        return host_path
    
    # Convert host absolute path to container path
    return os.path.join(Config.HOST_ROOT, host_path.lstrip('/'))

def convert_container_path_to_host(container_path):
    """Convert a container path back to host path for display."""
    if container_path.startswith(Config.HOST_ROOT):
        return '/' + container_path[len(Config.HOST_ROOT):].lstrip('/')
    return container_path

def initialize_database(db_manager, parser, embedder, folder_path):
    """
    Scans the specified folder, processes files, and populates the database.
    """
    print("\n--- Initializing Database ---")
    db_manager.clear_database()  # Clear existing data

    scanned_data = parser.scan_folder(folder_path)
    if not scanned_data:
        print("No files found or processed in the folder.")
        return

    print(f"\nProcessing {len(scanned_data)} sentences...")

    # Process in batches for efficiency
    batch_size = 32
    progress_bar = tqdm(total=len(scanned_data), desc="Vectorizing sentences", unit="sent")
    
    for i in range(0, len(scanned_data), batch_size):
        batch = scanned_data[i : i + batch_size]
        sentences = [item[1] for item in batch]
        # Convert container paths back to host paths for storage
        file_paths = [convert_container_path_to_host(item[0]) for item in batch]

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

    # Create necessary directories
    Config.ensure_directories()

    # Initialize components
    doc_parser = DocumentParser()
    embedder = EmbeddingModel(model_name=Config.MODEL_NAME)
    db_manager = VectorDB(
        db_path=Config.DB_FILE,
        embedding_dim=embedder.get_embedding_dimension(),
    )

    # Get folder path from user input
    print("\nEnter the folder path to scan for files.")
    print("You can use:")
    print("- Absolute path (e.g., /home/user/documents)")
    print("- Relative path (e.g., test_docs or ./test_docs)")
    folder_path = input("Folder path: ").strip()
    
    # Handle relative paths
    if not os.path.isabs(folder_path):
        # Check if we're running in Docker (if /app exists) or locally
        if os.path.exists("/app"):
            # Running in Docker container
            folder_path = os.path.join("/app", folder_path)
        else:
            # Running locally - use current working directory
            folder_path = os.path.abspath(folder_path)
    else:
        # Convert absolute host path to container path only if in Docker
        if os.path.exists("/app"):
            folder_path = convert_host_path_to_container(folder_path)
    
    print(f"\nScanning folder: {folder_path}")
    
    if not os.path.isdir(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist or is not accessible.")
        db_manager.close()
        sys.exit(1)

    initialize_database(db_manager, doc_parser, embedder, folder_path)

    # --- Perform Searches ---
    while True:
        try:
            query = input("\nEnter your search query (or 'q' to quit): ")
        except (EOFError, KeyboardInterrupt):
            break
            
        if not query:
            continue
            
        query = query.lower()
        if query in ('q', 'quit', 'exit'):
            break

        print(f"Searching for content related to: '{query}'")
        query_embedding = embedder.get_sentence_embedding(query)
        if query_embedding is None:
            print("Could not generate embedding for the query. Please try again.")
            continue

        search_results = db_manager.search_similar_sentences(
            query_embedding, 
            limit=Config.DEFAULT_SEARCH_LIMIT,
            distance_threshold=Config.DISTANCE_THRESHOLD
        )

        if not search_results:
            print("No relevant files found.")
        else:
            print("\n--- Top Relevant Files ---")
            relevant_files = set()
            for res in search_results:
                relevant_files.add(res["file_path"])

            for f_path in relevant_files:
                print(f"- {f_path}")

            print("\n--- Top Matching Sentences ---")
            for res in search_results:
                print(
                    f"  [File: {os.path.basename(res['file_path'])}] Sentence: '{res['sentence'][:70]}...' (Distance: {res['distance']:.4f})"
                )

    db_manager.close()
    print("\nApplication closed. Goodbye!")


if __name__ == "__main__":
    main()
