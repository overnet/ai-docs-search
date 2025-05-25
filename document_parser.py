import os
import re
import nltk
import xml.etree.ElementTree as ET
from nltk.tokenize import sent_tokenize
from PyPDF2 import PdfReader

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

    def parse_csv_file(self, file_path):
        """Reads a CSV file and returns its raw content as text."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return content
        except Exception as e:
            print(f"Error reading CSV {file_path}: {e}")
            return None

    def parse_xml_file(self, file_path):
        """Reads an XML file and returns its raw content as text."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return content
        except Exception as e:
            print(f"Error reading XML {file_path}: {e}")
            return None

    def parse_pdf_file(self, file_path):
        """Reads a PDF file and extracts all available text content."""
        try:
            # Create PDF reader object
            reader = PdfReader(file_path)
            
            # Extract text from all pages
            text_content = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_content.append(text.strip())
            
            # Join all text with newlines
            content = "\n".join(text_content)
            
            if not content.strip():
                print(f"Warning: No text content found in PDF file {file_path}")
                return None
                
            print(f"Extracted {len(text_content)} pages of text from PDF")
            return content
            
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
            return None

    def get_sentences(self, text):
        """Breaks a given text into sentences."""
        if not text:
            return []
            
        # Check if this is XML content
        if text.strip().startswith('<?xml'):
            # Split on closing tags and remove XML-specific content
            sentences = []
            # Remove XML declaration
            text = re.sub(r'<\?xml[^>]+\?>', '', text)
            # Remove namespace declarations
            text = re.sub(r'\sxmlns="[^"]+"', '', text)
            
            # Extract customer information
            customer_matches = re.finditer(r'<Customer[^>]*>.*?</Customer>', text, re.DOTALL)
            for match in customer_matches:
                customer_xml = match.group(0)
                company = re.search(r'<CompanyName>([^<]+)</CompanyName>', customer_xml)
                contact = re.search(r'<ContactName>([^<]+)</ContactName>', customer_xml)
                title = re.search(r'<ContactTitle>([^<]+)</ContactTitle>', customer_xml)
                if company:
                    customer_info = [f"Customer {company.group(1)}"]
                    if contact:
                        customer_info.append(f"contact person is {contact.group(1)}")
                    if title:
                        customer_info.append(f"who is {title.group(1)}")
                    sentences.append(" ".join(customer_info))
            
            # Extract order information
            order_matches = re.finditer(r'<Order>.*?</Order>', text, re.DOTALL)
            for match in order_matches:
                order_xml = match.group(0)
                customer_id = re.search(r'<CustomerID>([^<]+)</CustomerID>', order_xml)
                order_date = re.search(r'<OrderDate>([^<]+)</OrderDate>', order_xml)
                ship_date = re.search(r'ShippedDate="([^"]+)"', order_xml)
                freight = re.search(r'<Freight>([^<]+)</Freight>', order_xml)
                ship_address = re.search(r'<ShipAddress>([^<]+)</ShipAddress>', order_xml)
                ship_city = re.search(r'<ShipCity>([^<]+)</ShipCity>', order_xml)
                
                if customer_id:
                    # Find company name for this customer ID
                    company_match = re.search(
                        f'<Customer CustomerID="{customer_id.group(1)}"[^>]*>.*?<CompanyName>([^<]+)</CompanyName>',
                        text,
                        re.DOTALL
                    )
                    if company_match:
                        order_info = [f"{company_match.group(1)} placed an order"]
                        if order_date:
                            order_info.append(f"on {order_date.group(1).split('T')[0]}")
                        if ship_date:
                            order_info.append(f"which was shipped on {ship_date.group(1).split('T')[0]}")
                        if freight:
                            order_info.append(f"with shipping cost of ${freight.group(1)}")
                        if ship_address and ship_city:
                            order_info.append(f"to {ship_address.group(1)}, {ship_city.group(1)}")
                        sentences.append(" ".join(order_info))
            
            return sentences
            
        # For non-XML content, use regular sentence tokenization
        text = re.sub(r"\n+", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        sentences = sent_tokenize(text)
        return sentences

    def scan_folder(self, folder_path):
        """
        Scans a folder for supported files (.txt, .csv, .xml, .pdf),
        parses them, and returns a list of (file_path, sentence) tuples.
        """
        parsed_data = []
        if not os.path.isdir(folder_path):
            print(f"Error: Folder '{folder_path}' not found.")
            return []

        for root, _, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                
                if file_name.endswith(".txt"):
                    print(f"Processing TXT file: {file_path}")
                    content = self.parse_txt_file(file_path)
                elif file_name.endswith(".csv"):
                    print(f"Processing CSV file: {file_path}")
                    content = self.parse_csv_file(file_path)
                elif file_name.endswith(".xml"):
                    print(f"Processing XML file: {file_path}")
                    content = self.parse_xml_file(file_path)
                elif file_name.endswith(".pdf"):
                    print(f"Processing PDF file: {file_path}")
                    content = self.parse_pdf_file(file_path)
                else:
                    continue

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
