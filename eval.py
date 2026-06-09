from query import ask

evaluation_questions = [
    {
        "question": "What do students say about CS 225 workload and preparation?",
        "expected": "The system should mention data structures, C++, machine problems, starting early, and weekly time commitment.",
    },
    {
        "question": "What do students say about CS 128 workload and support resources?",
        "expected": "The system should mention workload, grade data, office hours, Even More Practice, quiz reviews, and practice problems.",
    },
    {
        "question": "What do students say about CS 374 difficulty and when to take it?",
        "expected": "The system should mention CS 374 is theory-heavy, depends on CS 173/proofs/math maturity, can be a time sink, and is easier with a strong group.",
    },
    {
        "question": "Which professors are described as helpful or good at teaching?",
        "expected": "The system should mention professors supported by the documents, such as Brad Solomon, Emily Fox, Wade Fagen-Ulmschneider, Margaret Fleck, Jeff Erickson, Alvarez, or Zilles.",
    },
    {
        "question": "What useful CS classes do students or alumni recommend for jobs?",
        "expected": "The system should mention CS 425, CS 411, CS 440, and ECE 391 if the correct source is retrieved.",
    },
    {
        "question": "What do students say about UIUC dining halls?",
        "expected": "The system should say it does not have enough information because the documents are about CS courses and professors, not dining halls.",
    },
]

for i, item in enumerate(evaluation_questions, start=1):
    print("\n" + "=" * 100)
    print(f"QUESTION {i}: {item['question']}")
    print("=" * 100)

    result = ask(item["question"])

    print("\nEXPECTED:")
    print(item["expected"])

    print("\nACTUAL:")
    print(result["answer"])

    print("\nSOURCES:")
    for source in result["sources"]:
        print(f"- {source}")

    print("\nRETRIEVED CHUNKS:")
    for chunk in result["retrieved_chunks"]:
        print(
            f"- {chunk['source']} | chunk {chunk['chunk_index']} | distance {chunk['distance']:.4f}"
        )