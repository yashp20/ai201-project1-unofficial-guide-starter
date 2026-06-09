from pathlib import Path
import re
import html
import random

# Folder where your 10 source documents are stored
DOCUMENTS_DIR = Path("documents")

# From planning.md
CHUNK_SIZE = 700
CHUNK_OVERLAP = 150


def clean_text(text: str) -> str:
    """
    Clean raw document text so the chunks only contain useful content.
    Removes HTML tags, decodes HTML entities, and normalizes spacing.
    """
    # Decode things like &amp; and &nbsp;
    text = html.unescape(text)

    # Remove HTML tags if any copied text includes them
    text = re.sub(r"<[^>]+>", " ", text)

    # Remove repeated whitespace/newlines
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def load_documents():
    """
    Load every .txt file from the documents folder.
    Returns a list of dictionaries with source filename and cleaned text.
    """
    documents = []

    if not DOCUMENTS_DIR.exists():
        raise FileNotFoundError(
            f"Could not find folder: {DOCUMENTS_DIR}. Make sure your folder is named 'documents'."
        )

    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        raw_text = file_path.read_text(encoding="utf-8")
        cleaned_text = clean_text(raw_text)

        if cleaned_text:
            documents.append(
                {
                    "source": file_path.name,
                    "text": cleaned_text,
                }
            )

    return documents


def chunk_text(text: str, source: str):
    """
    Split one document into overlapping chunks.
    Each chunk stores text, source filename, and chunk index.
    """
    chunks = []
    start = 0
    chunk_index = 0

    step = CHUNK_SIZE - CHUNK_OVERLAP

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()

        if len(chunk) > 0:
            chunks.append(
                {
                    "source": source,
                    "chunk_index": chunk_index,
                    "text": chunk,
                }
            )

        chunk_index += 1
        start += step

    return chunks


def build_chunks():
    """
    Load all documents and chunk them.
    Returns one list containing all chunks from all documents.
    """
    documents = load_documents()
    all_chunks = []

    for document in documents:
        chunks = chunk_text(document["text"], document["source"])
        all_chunks.extend(chunks)

    return all_chunks


def print_sample_chunks(chunks, sample_size=5):
    """
    Print representative chunks for Milestone 3 inspection.
    """
    if not chunks:
        print("No chunks were created.")
        return

    sample_size = min(sample_size, len(chunks))
    sample_chunks = random.sample(chunks, sample_size)

    print("\n===== SAMPLE CHUNKS =====\n")

    for i, chunk in enumerate(sample_chunks, start=1):
        print("=" * 80)
        print(f"Sample chunk #{i}")
        print(f"Source: {chunk['source']}")
        print(f"Chunk index: {chunk['chunk_index']}")
        print("-" * 80)
        print(chunk["text"])
        print()


if __name__ == "__main__":
    documents = load_documents()
    chunks = build_chunks()

    print(f"Loaded documents: {len(documents)}")
    print(f"Total chunks created: {len(chunks)}")

    print_sample_chunks(chunks, sample_size=5)

    print("\n===== CHECKPOINT =====")
    if len(chunks) == 0:
        print("Problem: No chunks were created. Check your documents folder and text files.")
    elif len(chunks) < 50:
        print("Warning: Fewer than 50 chunks. Your chunks may be too large or documents may be short.")
    elif len(chunks) > 2000:
        print("Warning: More than 2000 chunks. Your chunks may be too small.")
    else:
        print("Good: Chunk count is in a reasonable range.")