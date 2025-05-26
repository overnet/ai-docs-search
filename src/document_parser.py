import os
import re
import nltk
from nltk.tokenize import sent_tokenize
from PyPDF2 import PdfReader
from config import Config

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

    def parse_file(self, file_path):
        """Reads any supported file and returns its content as text."""
        try:
            # Handle PDF files differently
            if file_path.lower().endswith('.pdf'):
                reader = PdfReader(file_path)
                # Extract text from all pages
                text_content = []
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text.strip())
                content = "\n".join(text_content)
                if not content.strip():
                    print(f"Warning: No text content found in PDF file {file_path}")
                    return None
                print(f"Extracted {len(text_content)} pages of text from PDF")
                return content
            else:
                # For CSV and XML files, try different encodings
                encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
                file_ext = os.path.splitext(file_path)[1].lower()
                
                for encoding in encodings:
                    try:
                        with open(file_path, "r", encoding=encoding) as f:
                            content = f.read()
                            
                            # Basic validation for XML files
                            if file_ext == '.xml':
                                if not content.strip().startswith('<?xml') and not content.strip().startswith('<'):
                                    print(f"Warning: File {file_path} doesn't appear to be valid XML")
                                    continue
                            
                            # Basic validation for CSV files
                            elif file_ext == '.csv':
                                # Check if it has some basic CSV structure (commas or semicolons)
                                if ',' not in content and ';' not in content:
                                    print(f"Warning: File {file_path} doesn't appear to be valid CSV")
                                    continue
                            
                            print(f"Successfully read file with {encoding} encoding")
                            return content
                    except UnicodeDecodeError:
                        if encoding == encodings[-1]:  # Last encoding attempt
                            print(f"Error: Could not decode {file_path} with any supported encoding")
                            return None
                        continue
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
                        return None
                        
                return None
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None

    def get_sentences(self, text):
        """Breaks a given text into sentences."""
        if not text:
            return []
            
        # Clean up the text
        text = re.sub(r"\n+", " ", text)  # Replace newlines with spaces
        text = re.sub(r"\s+", " ", text).strip()  # Normalize whitespace
        
        # Break into sentences
        sentences = sent_tokenize(text)
        return sentences

    def scan_folder(self, folder_path):
        """
        Scans a folder for supported files,
        reads them as text, and returns a list of (file_path, sentence) tuples.
        """
        parsed_data = []
        if not os.path.isdir(folder_path):
            print(f"Error: Folder '{folder_path}' not found.")
            return []

        for root, _, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_ext = os.path.splitext(file_name)[1].lower()
                
                if file_ext not in Config.SUPPORTED_EXTENSIONS:
                    continue
                
                print(f"Processing {file_ext[1:].upper()} file: {file_path}")
                content = self.parse_file(file_path)

                if content:
                    sentences = self.get_sentences(content)
                    for sentence in sentences:
                        # Filter out very short or empty sentences that might be noise
                        if len(sentence.strip()) > Config.MIN_SENTENCE_LENGTH:
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
