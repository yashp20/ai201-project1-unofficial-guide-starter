import os
from dotenv import load_dotenv
from groq import Groq

from retrieval import load_vector_store, retrieve


load_dotenv()

MODEL_NAME = "llama-3.3-70b-versatile"
TOP_K = 5


def format_context(retrieved_chunks):
    """
    Format retrieved chunks into context for the LLM.
    Each chunk includes source metadata so the model can stay grounded.
    """
    context_parts = []

    for i, chunk in enumerate(retrieved_chunks, start=1):
        context_parts.append(
            f"[Source {i}: {chunk['source']} | Chunk {chunk['chunk_index']}]\n"
            f"{chunk['text']}"
        )

    return "\n\n".join(context_parts)


def unique_sources(retrieved_chunks):
    """
    Return unique source filenames from retrieved chunks.
    This guarantees source attribution even if the LLM forgets to cite.
    """
    sources = []

    for chunk in retrieved_chunks:
        source = chunk["source"]
        if source not in sources:
            sources.append(source)

    return sources


def generate_answer(question, retrieved_chunks):
    """
    Generate a grounded answer using only retrieved context.
    """
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("Missing GROQ_API_KEY. Add it to your .env file.")

    client = Groq(api_key=api_key)

    context = format_context(retrieved_chunks)

    system_prompt = """
You are a grounded RAG assistant for an unofficial UIUC CS course guide.

Rules:
1. Answer ONLY using the provided retrieved document context.
2. Do NOT use outside knowledge.
3. If the provided context does not contain enough information, say:
   "I don't have enough information on that from the provided documents."
4. Mention the source filenames when explaining your answer.
5. Do not invent professor names, course facts, statistics, or opinions.
"""

    user_prompt = f"""
Question:
{question}

Retrieved context:
{context}

Answer the question using only the retrieved context.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()},
        ],
        temperature=0.1,
    )

    return response.choices[0].message.content


def ask(question):
    """
    End-to-end RAG function:
    query -> retrieve chunks -> generate grounded answer -> return sources.
    """
    collection, model = load_vector_store()

    retrieved_chunks = retrieve(
        query=question,
        collection=collection,
        model=model,
        top_k=TOP_K,
    )

    answer = generate_answer(question, retrieved_chunks)
    sources = unique_sources(retrieved_chunks)

    return {
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieved_chunks,
    }


if __name__ == "__main__":
    test_questions = [
        "What do students say about CS 374 difficulty?",
        "What do students say about CS 128 support resources?",
        "What do students say about dining halls at UIUC?",
    ]

    for question in test_questions:
        print("\n" + "=" * 100)
        print(f"QUESTION: {question}")
        print("=" * 100)

        result = ask(question)

        print("\nANSWER:")
        print(result["answer"])

        print("\nSOURCES:")
        for source in result["sources"]:
            print(f"- {source}")

        print("\nRETRIEVED CHUNKS:")
        for chunk in result["retrieved_chunks"]:
            print(
                f"- {chunk['source']} | chunk {chunk['chunk_index']} | distance {chunk['distance']:.4f}"
            )