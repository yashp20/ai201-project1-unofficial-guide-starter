from pathlib import Path
import shutil

import chromadb
from sentence_transformers import SentenceTransformer

from ingest import build_chunks


CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "uiuc_cs_reviews"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 5


def reset_chroma_db():
    """
    Delete old ChromaDB data so we can rebuild the vector store cleanly.
    """
    chroma_path = Path(CHROMA_DIR)

    if chroma_path.exists():
        shutil.rmtree(chroma_path)


def get_embedding_model():
    """
    Load the local embedding model.
    """
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def build_vector_store():
    """
    Load chunks from ingest.py, embed them, and store them in ChromaDB.
    """
    print("Loading chunks...")
    chunks = build_chunks()
    print(f"Loaded {len(chunks)} chunks.")

    if not chunks:
        raise ValueError("No chunks found. Run ingest.py first and check your documents.")

    print("Loading embedding model...")
    model = get_embedding_model()

    documents = [chunk["text"] for chunk in chunks]
    ids = [f"{chunk['source']}_{chunk['chunk_index']}" for chunk in chunks]
    metadatas = [
        {
            "source": chunk["source"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]

    print("Creating embeddings...")
    embeddings = model.encode(documents).tolist()

    print("Resetting ChromaDB...")
    reset_chroma_db()

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    print("Adding chunks to ChromaDB...")
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Vector store built successfully.")
    print(f"Stored chunks: {collection.count()}")

    return collection, model


def load_vector_store():
    """
    Load existing ChromaDB collection.
    """
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    model = get_embedding_model()

    return collection, model


def retrieve(query: str, collection, model, top_k: int = TOP_K):
    """
    Retrieve the top-k most relevant chunks for a query.
    Returns chunks, metadata, and distance scores.
    """
    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    retrieved_chunks = []

    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        retrieved_chunks.append(
            {
                "text": document,
                "source": metadata["source"],
                "chunk_index": metadata["chunk_index"],
                "distance": distance,
            }
        )

    return retrieved_chunks


def print_results(query: str, retrieved_chunks):
    """
    Print retrieval results in a readable format.
    """
    print("\n" + "=" * 100)
    print(f"QUERY: {query}")
    print("=" * 100)

    for i, chunk in enumerate(retrieved_chunks, start=1):
        print(f"\nResult #{i}")
        print(f"Source: {chunk['source']}")
        print(f"Chunk index: {chunk['chunk_index']}")
        print(f"Distance: {chunk['distance']:.4f}")
        print("-" * 100)
        print(chunk["text"])


if __name__ == "__main__":
    collection, model = build_vector_store()

    test_queries = [
        "What do students say about CS 225 workload and preparation?",
        "What do students say about CS 128 workload and support resources?",
        "What do students say about CS 374 difficulty and when to take it?",
    ]

    for query in test_queries:
        results = retrieve(query, collection, model, top_k=TOP_K)
        print_results(query, results)

    print("\n===== CHECKPOINT =====")
    print("Check that each query returns chunks related to the question.")
    print("Top distance scores should ideally be below 0.5.")