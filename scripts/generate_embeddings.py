import os
import json
from typing import List
import PyPDF2
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'
    return text

def create_chunks(text: str, chunk_size: int = 700, chunk_overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_text(text)
    return chunks

def generate_embeddings(chunks: List[str], model_name: str = 'all-MiniLM-L6-v2') -> np.ndarray:
    """Generate embeddings for text chunks using sentence-transformers."""
    model = SentenceTransformer(f'sentence-transformers/{model_name}')
    embeddings = model.encode(chunks, show_progress_bar=True)
    return embeddings

def main():
    # Create necessary directories
    os.makedirs('src/lib/chunks', exist_ok=True)
    os.makedirs('src/lib/embeddings', exist_ok=True)

    # Path to your handbook PDFs
    handbook_dir = 'handbooks'
    if not os.path.exists(handbook_dir):
        os.makedirs(handbook_dir)
        print(f"Please place your handbook PDFs in the '{handbook_dir}' directory and run this script again.")
        return

    # Combine all handbook texts
    combined_text = ''
    for filename in os.listdir(handbook_dir):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(handbook_dir, filename)
            print(f"Processing {filename}...")
            text = extract_text_from_pdf(pdf_path)
            combined_text += text + '\n\n'

    # Create chunks
    print("Creating chunks...")
    chunks = create_chunks(combined_text)

    # Generate embeddings
    print("Generating embeddings...")
    embeddings = generate_embeddings(chunks)

    # Save chunks and embeddings
    print("Saving chunks and embeddings...")
    with open('src/lib/chunks/chunks.json', 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    embeddings_list = embeddings.tolist()
    with open('src/lib/embeddings/embeddings.json', 'w', encoding='utf-8') as f:
        json.dump(embeddings_list, f)

    print("Done! Created the following files:")
    print("- src/lib/chunks/chunks.json")
    print("- src/lib/embeddings/embeddings.json")
    print(f"\nTotal chunks created: {len(chunks)}")

if __name__ == "__main__":
    main() 