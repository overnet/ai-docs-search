import os
import re
import nltk
from nltk.tokenize import sent_tokenize

# Download required NLTK data if not already present
required_nltk_data = ['punkt', 'punkt_tab']
for data in required_nltk_data:
    try:
        nltk.data.find(f"tokenizers/{data}")
    except LookupError:
        nltk.download(data)


class DocumentParser:
    def __init__(self):
        pass

    def parse_txt_file(self, file_path):
        """Reads a .txt file and returns its content."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return content
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None

    def get_sentences(self, text):
        """Breaks a given text into sentences."""
        if not text:
            return []
        # Basic cleanup: remove extra newlines, multiple spaces
        text = re.sub(r"\n+", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        sentences = sent_tokenize(text)
        return sentences

    def scan_folder(self, folder_path):
        """
        Scans a folder for .txt files, parses them, and returns
        a list of (file_path, sentence) tuples.
        """
        parsed_data = []
        if not os.path.isdir(folder_path):
            print(f"Error: Folder '{folder_path}' not found.")
            return []

        for root, _, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith(".txt"):
                    file_path = os.path.join(root, file_name)
                    print(f"Processing file: {file_path}")
                    content = self.parse_txt_file(file_path)
                    if content:
                        sentences = self.get_sentences(content)
                        for sentence in sentences:
                            # Filter out very short or empty sentences that might be noise
                            if len(sentence.strip()) > 10:
                                parsed_data.append((file_path, sentence.strip()))
        return parsed_data


# Example usage (for testing this module independently)
if __name__ == "__main__":
    parser = DocumentParser()
    # Create a dummy folder and files for testing
    test_folder = "test_docs"
    os.makedirs(test_folder, exist_ok=True)
    with open(os.path.join(test_folder, "doc1.txt"), "w") as f:
        f.write(
            "This is the first sentence. It talks about dogs. Dogs are fluffy. The quick brown fox jumps over the lazy dog."
        )
    with open(os.path.join(test_folder, "doc2.txt"), "w") as f:
        f.write(
            "Cats are independent animals. They love to sleep. A cat purrs when it is happy. The elephant is a large mammal."
        )
    with open(os.path.join(test_folder, "empty.txt"), "w") as f:
        f.write("")

    sentences_data = parser.scan_folder(test_folder)
    print("\n--- Scanned Sentences ---")
    for fp, sent in sentences_data:
        print(f"File: {os.path.basename(fp)}, Sentence: {sent[:50]}...")
